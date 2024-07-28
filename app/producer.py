from flask import Flask, Blueprint, request, jsonify
from kafka import KafkaProducer
import json
import logging
import re
from uuid import UUID

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app and blueprint
app = Flask(__name__)
main_blueprint = Blueprint('main', __name__)


# Kafka Producer setup
class KafkaProducerService:
    def __init__(self, bootstrap_servers, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def publish_message(self, key, value):
        def on_send_success(record_metadata):
            logger.info(
                f'Message sent to {record_metadata.topic} partition: {record_metadata.partition} offset: {record_metadata.offset}')

        def on_send_error(excp):
            logger.error(f'Error sending message: {excp}')

        logger.info(f'Sending message: {value}')
        self.producer.send(self.topic, key=key, value=value).add_callback(on_send_success).add_errback(on_send_error)
        self.producer.flush()