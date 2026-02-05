from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import Text, TextInfo, Button, ButtonInfo
from paho.mqtt.client import Client, MQTTMessage
import csv
import logging
import random
import sys
import time

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# Configure the required parameters for the MQTT broker
mqtt_settings = Settings.MQTT(
        host="172.17.0.1",
        mqtt_prefix="homeassistant")

device_info = DeviceInfo(
        name="qotd",
        model="Custom",
        manufacturer="github.com/trixing",
        identifiers="qotd_id")

quote_info = TextInfo(name="Quote", object_id="qotd_quote", unique_id="qotd_text_id", device=device_info)
author_info = TextInfo(name="Author", object_id="qotd_author", unique_id="qotd_author_id", device=device_info)
btn_info = ButtonInfo(name="Regenerate", object_id="qotd_regen", unique_id="qotd_regen_id", device=device_info)

quote_settings = Settings(mqtt=mqtt_settings, entity=quote_info)
btn_settings = Settings(mqtt=mqtt_settings, entity=btn_info)
author_settings = Settings(mqtt=mqtt_settings, entity=author_info)

quotes = []
def read_quotes():
    with open('quotes_short.csv') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        for l in reader:
            quote, author = l
            quotes.append((quote, author))
read_quotes()
 
def regenerate():
    quote, author = random.choice(quotes)
    logging.info(f"New quote {quote} by {author}")
    my_quote.set_text(quote)
    my_author.set_text(author)

def quote_callback(client: Client, user_data, message: MQTTMessage):
    text = message.payload.decode()
    logging.info(f"Received {text} from HA")

def btn_callback(client: Client, user_data, message: MQTTMessage):
    logging.info(f"Received button from HA")
    regenerate()

# Define an optional object to be passed back to the callback
user_data = {}

my_button = Button(btn_settings, btn_callback, user_data)
# Instantiate the text
my_quote = Text(quote_settings, quote_callback, user_data)
my_author = Text(author_settings, quote_callback, user_data)
# Set the initial text displayed in HA UI, publishing an MQTT message that gets picked up by HA
regenerate()

my_button.write_config()

while True:
    time.sleep(1)
