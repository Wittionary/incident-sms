FROM python:3
LABEL maintainer="Witt Allen @wittionary"
ADD incident-sms.py /
ADD clients.json /
ADD config.json /
RUN pip install twilio
CMD [ "python", "./incident-sms.py"]
