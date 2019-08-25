# sonarr_netimport
A sloppy code written in python to fetch TV series from TVDB and add it to sonarr.
It can send email notification in case of an error with sync.

Root folder for sonarr should be `/tv`.  
All TV series are added to `any` sonarr profile.  
If you want to change these two things, you can do it in the code, in the section;
```python
sonarr_post_params = {
                'addOptions': {'searchForMissingEpisodes': True},
                'qualityProfileId': 1,  # Profile: any
                'monitored': True,
                'rootFolderPath': '/tv/'
            }
```

# Config
Script variables are passed as environment variables. Supported variables are;

#### Mandatory
* TVDB_USERNAME: TVDB account username
* TVDB_API_KEY: TVDB API key. You will be able to get this with your account
* SONARR_IP: IP address where sonarr is listening
* SONARR_PORT: Port number for sonarr. default is 8989
* SONARR_API_KEY: API key for sonarr
* SYNC_INTERVAL: Interval at which to sync tv series from TVBD with sonarr in seconds

#### Optional. These are for email notification
* EMAIL_ADDRESS: Sender email address
* EMAIL_TO_ADDRESS: Recipient email account 
* EMAIL_PASSWORD: Sender email address password
* SMTP_SERVER: smtp server. Example for gmail: smtp.gmail.com
* SMTP_SERVER_PORT: Port number for smtp server

# Docker Image
Docker image is available at https://hub.docker.com/r/thundermagic/sonarr_netimport
#### Example docker compose
```yaml
version: "2"
services:
    sonarr_netimport:
        image: thundermagic/sonarr_netimport:arm32v7-latest
        restart: on-failure
        container_name: sonarr_netimport
        environment:
          - TVDB_USERNAME=first.last
          - TVDB_USER_KEY=user_key
          - TVDB_API_KEY=api_key
          - SONARR_IP=192.168.4.4
          - SONARR_PORT=8989
          - SONARR_API_KEY=sonarr_key
          - SYNC_INTERVAL=3600  # Interval at which to sync with TVDB, in seconds
          # Below variables are for sending error notification emails. If not needed, delete these
          - EMAIL_ADDRESS=first.last@gmail.com
          - EMAIL_TO_ADDRESS=first.last@gmail.com
          - EMAIL_PASSWORD=gmail_app_password
          - SMTP_SERVER=smtp.gmail.com
          - SMTP_SERVER_PORT=587
```
