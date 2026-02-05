# docker build -t trixing/qotd .
FROM python:3.14-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./qotd_mqtt_service.py" ]
