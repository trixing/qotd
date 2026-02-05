## Dataset
Kaggle Quotes 500k
https://www.kaggle.com/datasets/manann/quotes-500k?resource=download

## Build
docker build -t trixing/qotd .

## Run
docker run --name trixing_qotd --restart=always --detach trixing/qotd

## Debug
docker run -it -e MQTT_PREFIX=development -v $PWD:/usr/src/app  trixing/qotd

## Develop
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 qotd_mqtt_service.py

### Environment Variables
Configure the service using environment variables:

- `MQTT_HOST`: MQTT broker host (default: `172.17.0.1`)
- `MQTT_PREFIX`: MQTT discovery prefix (default: `homeassistant`)
- `ENTITY_PREFIX`: Prefix for entity object_id, unique_id, and identifiers (default: `qotd`)

Example with custom MQTT prefix:
```bash
MQTT_HOST=192.168.1.100 MQTT_PREFIX=development ENTITY_PREFIX=myquote python3 qotd_mqtt_service.py
```