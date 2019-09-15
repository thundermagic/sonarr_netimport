# sonarr_netimport
A sloppy code written in python to fetch TV series from TVDB and add it to sonarr.
It can send email notification in case of an error with sync.

# Config
Script variables are passed as environment variables. Supported variables are;

#### Mandatory
* TVDB_USERNAME: TVDB account username
* TVDB_API_KEY: TVDB API key. You will be able to get this with your account
* SONARR_IP: IP address where sonarr is listening
* SONARR_PORT: Port number for sonarr. default is 8989
* SONARR_API_KEY: API key for sonarr
* SYNC_INTERVAL: Interval at which to sync tv series from TVBD with sonarr in seconds
* SEARCH_MISSING_EPISODES: If to search for missing episode. Enter 1 for True. Any other value is False
* QUALITY_PROFILE_ID: Quality profile. Profile `any` has ID of 1.
* MONITORED: If to monitor the series. Enter 1 for True. Any other value is False
* ROOT_FOLDER_PATH: root folder where series will be stored.

#### Optional. These are for email notification
* EMAIL_ADDRESS: Sender email address
* EMAIL_TO_ADDRESS: Recipient email account 
* EMAIL_PASSWORD: Sender email address password
* SMTP_SERVER: smtp server. Example for gmail: smtp.gmail.com
* SMTP_SERVER_PORT: Port number for smtp server

# Docker Image
Docker image is available at: https://hub.docker.com/r/thundermagic/sonarr_netimport.  
Docker image is multi arch. Supported architectures are `arm` and `amd64`.  
Docker manifest is used for multi arch awareness. So you just need to pull the image regardless of the underlying platform and the correct image will be pulled.  

#### Example docker compose
```yaml
version: "2"
services:
    sonarr_netimport:
        image: thundermagic/sonarr_netimport:latest
        restart: on-failure
        container_name: sonarr_netimport
        environment:
          - TVDB_USERNAME=first.last
          - TVDB_USER_KEY=user_key
          - TVDB_API_KEY=tvdb_api_key
          # IP address and port number where sonarr can be accessed
          - SONARR_IP=192.168.4.4
          - SONARR_PORT=8989
          # Sonarr app API key. This is on sonarr under settings>general
          - SONARR_API_KEY=sonarr_key
          - SYNC_INTERVAL=3600  # Interval at which to sync with TVDB, in seconds
          - SEARCH_MISSING_EPISODES=1  # 1 is True
          - QUALITY_PROFILE_ID=1  # 1 is profile any
          - MONITORED=1  # 1 is True
          - ROOT_FOLDER_PATH=/tv/  # Full path of root folder
          # Below variables are for sending error notification emails. If not needed, delete these
          - EMAIL_ADDRESS=first.last@gmail.com
          - EMAIL_TO_ADDRESS=first.last@gmail.com
          - EMAIL_PASSWORD=gmail_app_password
          - SMTP_SERVER=smtp.gmail.com
          - SMTP_SERVER_PORT=587
```
