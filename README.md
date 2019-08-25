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

#Config
Script variables are passed as environment variables. Supported variables are;

####Mandatory
* TVDB_USERNAME: TVDB account username
* TVDB_API_KEY: TVDB API key. You will be able to get this with your account
* SONARR_IP: IP address where sonarr is listening
* SONARR_PORT: Port number for sonarr. default is 8989
* SONARR_API_KEY: API key for sonarr
* SYNC_INTERVAL: Interval to which to sync tv series from TVBD with sonarr

####Optional. These are for email notification
* EMAIL_ADDRESS: Sender email address
* EMAIL_TO_ADDRESS: Recipient email account 
* EMAIL_PASSWORD: Sender email address password
* SMTP_SERVER: smtp server. Example for gmail: smtp.gmail.com
* SMTP_SERVER_PORT: Port number for smtp server

