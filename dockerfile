# Order is attempting to optimize for cache hit
FROM python:3.6
LABEL maintainer="Witt Allen @wittionary"
ADD requirements.txt /
RUN pip install -r requirements.txt

ADD /static/css/style.css /static/css/style.css
ADD /templates/index.html /templates/index.html
ADD /templates/navigation.html /templates/navigation.html
ADD /templates/response.html /templates/response.html

ADD config.json /
ADD clients.json /
ADD incident-sms.py /

EXPOSE 5000
ENTRYPOINT [ "python", "./incident-sms.py"]
