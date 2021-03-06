import requests
import smtplib
import os
from time import sleep
from email.message import EmailMessage


def send_email(message):
    """ Sends email """

    msg = EmailMessage()
    msg['Subject'] = 'Sonarr failure'
    msg['From'] = email_address
    msg['To'] = email_to_address

    msg.set_content('Sonarr netimport list failure\n\n'
                    'Error msg: {0}'.format(message))

    with smtplib.SMTP(smtp_server, int(smtp_server_port)) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
    print('email sent')
    return None


def get_tvdb_jwt():

    login_post = {"apikey": tvdb_api_key, "username": tvdb_username, "userkey": tvdb_user_key}
    login_url = 'https://api.thetvdb.com/login'
    jwt = requests.post(login_url, json=login_post)
    return jwt.json()['token']


def get_tvdb_show_ids() -> set:
    """ Returns tvdbId of shows in TVDB list """

    jwt = get_tvdb_jwt()
    auth = {'Authorization': 'Bearer {0}'.format(jwt)}
    shows = requests.get('https://api.thetvdb.com/user/favorites', headers=auth)
    show_names = shows.json()['data']['favorites']
    show_ids = []
    for show in show_names:
        search_show = requests.get('https://api.thetvdb.com/search/series', headers=auth, params={
            'name': show
        })
        for resp in search_show.json()['data']:
            show_ids.append(resp['id'])
    return set([int(show_id) for show_id in show_ids])


def get_show_ids_from_sonarr() -> set:
    """ Return tvdbId of shows already in sonarr """

    shows = requests.get(sonarr_url, headers=sonarr_headers).json()
    show_ids = [show['tvdbId'] for show in shows]
    return set(show_ids)


def add_shows_sonarr(tvdb_shows: set) -> dict:
    result = {}
    for show_id in tvdb_shows:
        sonarr_post_params['tvdbId'] = show_id
        resp = requests.post(sonarr_url, headers=sonarr_headers, json=sonarr_post_params)
        result[show_id] = resp.status_code
    return result


if __name__ == '__main__':

    sync_interval = os.environ.get('SYNC_INTERVAL')
    if sync_interval is None:
        raise ValueError('Sync interval cannot be empty')

    tvdb_username = os.environ.get('TVDB_USERNAME')
    tvdb_user_key = os.environ.get('TVDB_USER_KEY')
    tvdb_api_key = os.environ.get('TVDB_API_KEY')

    sonarr_ip = os.environ.get('SONARR_IP')
    sonarr_port = os.environ.get('SONARR_PORT')
    sonarr_api_key = os.environ.get('SONARR_API_KEY')

    search_missing_episodes = os.environ.get('SEARCH_MISSING_EPISODES')  # 1: True, any other value is False
    quality_profile_id = os.environ.get('QUALITY_PROFILE_ID')  # Profile `any` is 1
    monitored = os.environ.get('MONITORED')  # 1: True, any other value is False
    root_folder_path = os.environ.get('ROOT_FOLDER_PATH')

    if tvdb_username is None \
            or tvdb_user_key is None \
            or tvdb_api_key is None \
            or sonarr_ip is None \
            or sonarr_port is None \
            or sonarr_api_key is None \
            or search_missing_episodes is None \
            or quality_profile_id is None \
            or monitored is None \
            or root_folder_path is None:
        raise ValueError('Mandatory variables cannot be empty')

    email_address = os.environ.get('EMAIL_ADDRESS')
    email_to_address = os.environ.get('EMAIL_TO_ADDRESS')
    email_password = os.environ.get('EMAIL_PASSWORD')
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_server_port = os.environ.get('SMTP_SERVER_PORT')

    while True:
        try:
            print('Sleeping for {0} seconds'.format(sync_interval))
            print()
            sleep(int(sync_interval))

            sonarr_headers = {
                'X-API-KEY': sonarr_api_key
            }
            sonarr_url = 'http://{ip}:{port}/api/series'.format(ip=sonarr_ip, port=sonarr_port)

            sonarr_post_params = {
                'addOptions': {'searchForMissingEpisodes': True if int(search_missing_episodes) == 1 else False},
                'qualityProfileId': int(quality_profile_id),  # Profile: 1 corresponds to `any` profile
                'monitored': True if int(monitored) == 1 else False,
                'rootFolderPath': root_folder_path  # full folder path (example: /tv/)
            }

            print('Getting shows from TVDB')
            tvdb_shows = get_tvdb_show_ids()
            print('Shows in TVDB list: {0}'.format(tvdb_shows))

            print('Getting shows from sonarr')
            sonarr_shows = get_show_ids_from_sonarr()
            print('Shows in sonarr: {0}'.format(sonarr_shows))

            shows_to_add = tvdb_shows.difference(sonarr_shows)
            if shows_to_add:
                print('Shows to add to sonarr: {0}'.format(shows_to_add))
                print('Adding shows to sonarr')
                add_result = add_shows_sonarr(shows_to_add)
                print('Show add result: {0}'.format(add_result))

                failed = {}
                for show_id, status_code in add_result.items():
                    if status_code != 201:
                        failed[show_id] = status_code

                if failed:
                    if email_address is None \
                            or email_password is None \
                            or smtp_server is None \
                            or smtp_server_port is None:
                        pass
                    else:
                        print('sending email notification')
                        send_email('Show failed to be added: {0}'.format(failed))
            else:
                print('No shows to add to sonarr')
        except Exception:
            print('Unexpected error')
            raise
