FROM python:3.6-alpine

RUN pip install requests

COPY ./sonarr_netimport.py .

CMD [ "python", "./sonarr_netimport.py" ]