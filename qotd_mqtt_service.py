from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import Text, TextInfo, Button, ButtonInfo
from paho.mqtt.client import Client, MQTTMessage
import csv
import logging
import random
import sys
import time

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


class QuoteOfTheDayService:
    """MQTT service for publishing a quote of the day."""

    def __init__(self, mqtt_host: str = "172.17.0.1", quotes_file: str = "quotes_short.csv"):
        """Initialize the QOTD service.
        
        Args:
            mqtt_host: MQTT broker host address
            quotes_file: Path to CSV file containing quotes
        """
        self.mqtt_host = mqtt_host
        self.quotes_file = quotes_file
        self.quotes = []
        
        # Configure MQTT and device settings
        self.mqtt_settings = Settings.MQTT(
            host=mqtt_host,
            mqtt_prefix="homeassistant"
        )
        
        self.device_info = DeviceInfo(
            name="qotd",
            model="Custom",
            manufacturer="github.com/trixing",
            identifiers="qotd_id"
        )
        
        # Initialize MQTT entities
        self._initialize_entities()
        
        # Load quotes
        self._load_quotes()
        
        # Publish initial quote
        self.regenerate()
        
        # Register button config
        self.button.write_config()
    
    def _initialize_entities(self):
        """Initialize all MQTT text and button entities."""
        quote_info = TextInfo(
            name="Quote",
            object_id="qotd_quote",
            unique_id="qotd_quote_id",
            device=self.device_info
        )
        author_info = TextInfo(
            name="Author",
            object_id="qotd_author",
            unique_id="qotd_author_id",
            device=self.device_info
        )
        tags_info = TextInfo(
            name="Tags",
            object_id="qotd_tags",
            unique_id="qotd_tags_id",
            device=self.device_info
        )
        vestaboard_info = TextInfo(
            name="Vestaboard Quote Fit",
            object_id="qotd_vestaboard_fit",
            unique_id="qotd_vestaboard_fit_id",
            device=self.device_info
        )
        btn_info = ButtonInfo(
            name="Regenerate",
            object_id="qotd_regen",
            unique_id="qotd_regen_id",
            device=self.device_info
        )
        
        quote_settings = Settings(mqtt=self.mqtt_settings, entity=quote_info)
        author_settings = Settings(mqtt=self.mqtt_settings, entity=author_info)
        tags_settings = Settings(mqtt=self.mqtt_settings, entity=tags_info)
        vestaboard_settings = Settings(mqtt=self.mqtt_settings, entity=vestaboard_info)
        btn_settings = Settings(mqtt=self.mqtt_settings, entity=btn_info)
        
        self.quote = Text(quote_settings, self._quote_callback)
        self.author = Text(author_settings, self._quote_callback)
        self.tags = Text(tags_settings, self._quote_callback)
        self.vestaboard = Text(vestaboard_settings, self._quote_callback)
        self.button = Button(btn_settings, self._button_callback)
    
    def _load_quotes(self):
        """Load quotes from CSV file."""
        with open(self.quotes_file) as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            for row in reader:
                self.quotes.append(list(row))
        logging.info(f"Loaded {len(self.quotes)} quotes from {self.quotes_file}")
    
    def regenerate(self):
        """Select and publish a random quote."""
        
        quote_text, author_text, tags_text, vestaboard_fit = random.choice(self.quotes)
        logging.info(f"New quote: {quote_text} by {author_text}")
        
        self.quote.set_text(quote_text)
        self.author.set_text(author_text)
        self.tags.set_text(tags_text)
        self.vestaboard.set_text(vestaboard_fit)
    
    def _quote_callback(self, client: Client, user_data, message: MQTTMessage):
        """Handle incoming quote messages from HA."""
        text = message.payload.decode()
        logging.info(f"Received callback: {text}")
    
    def _button_callback(self, client: Client, user_data, message: MQTTMessage):
        """Handle regenerate button press from HA."""
        logging.info("Regenerate button pressed")
        self.regenerate()
    
    def run(self):
        """Run the service main loop."""
        logging.info("Starting QOTD service...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Service stopped")


if __name__ == "__main__":
    service = QuoteOfTheDayService()
    service.run()
