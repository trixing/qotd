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

quote_info = TextInfo(
    name="Quote",
    object_id="qotd_quote",
    unique_id="qotd_quote_id",
    device=device_info)
author_info = TextInfo(
    name="Author",
    object_id="qotd_author",
    unique_id="qotd_author_id",
    device=device_info)
tags_info = TextInfo(
    name="Tags",
    object_id="qotd_tags",
    unique_id="qotd_tags_id",
    device=device_info)
vestaboard_info = TextInfo(
    name="Vestaboard Quote Fit",
    object_id="qotd_vestaboard_fit",
    unique_id="qotd_vestaboard_fit_id",
    device=device_info)
btn_info = ButtonInfo(
    name="Regenerate",
    object_id="qotd_regen",
    unique_id="qotd_regen_id",
    device=device_info)

quote_settings = Settings(mqtt=mqtt_settings, entity=quote_info)
btn_settings = Settings(mqtt=mqtt_settings, entity=btn_info)
author_settings = Settings(mqtt=mqtt_settings, entity=author_info)
vestaboard_settings = Settings(mqtt=mqtt_settings, entity=vestaboard_info)
tags_settings = Settings(mqtt=mqtt_settings, entity=tags_info)

quotes = []
def read_quotes():
    with open('quotes_short.csv') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        for l in reader:
            quotes.append(list(l))
read_quotes()
 
def regenerate():
    x = random.choice(quotes)
    print(x)
    quote, author, tags, vestaboard_fit = x
    logging.info(f"New quote {quote} by {author}")

    my_quote.set_text(quote)
    my_author.set_text(author)
    my_tags.set_text(tags)
    my_vestaboard.set_text(vestaboard_fit)

def quote_callback(client: Client, user_data, message: MQTTMessage):
    text = message.payload.decode()
    logging.info(f"Received {text} from HA")

def btn_callback(client: Client, user_data, message: MQTTMessage):
    logging.info(f"Received button from HA")
    regenerate()

# Define an optional object to be passed back to the callback
user_data = {}

my_button = Button(btn_settings, btn_callback)
# Instantiate the text
my_quote = Text(quote_settings, quote_callback)
my_author = Text(author_settings, quote_callback)
my_vestaboard = Text(vestaboard_settings, quote_callback)
my_tags = Text(tags_settings, quote_callback)
# Set the initial text displayed in HA UI, publishing an MQTT message that gets picked up by HA
regenerate()

my_button.write_config()

while True:
    time.sleep(1)
