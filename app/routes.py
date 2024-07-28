from flask import Flask, Blueprint, request, jsonify
from kafka import KafkaProducer
import json
import logging
from uuid import UUID
import re


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

        # Callback for success
        def on_send_success(record_metadata):
            logger.info(
                f'Message sent to {record_metadata.topic} partition: {record_metadata.partition} offset: {record_metadata.offset}')

        # Callback for error
        def on_send_error(excp):
            logger.error(f'Error sending message: {excp}')

        # Send the message
        logger.info(f'Sending message: {value}')
        self.producer.send(self.topic, key=key, value=value).add_callback(on_send_success).add_errback(on_send_error)
        self.producer.flush()


# Endpoint to start session
# Endpoint to start session
@main_blueprint.route('/api/start_session', methods=['POST'])
def start_session():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request format, JSON expected"}), 400

    station_id = data.get('station_id')
    driver_token = data.get('driver_token')

    # Validate station_id as UUIDv4
    try:
        uuid_obj = UUID(station_id, version=4)
    except ValueError:
        return jsonify({"error": "Invalid station_id, must be a valid UUIDv4"}), 400

    # Validate driver_token
    if not driver_token or not (20 <= len(driver_token) <= 80):
        return jsonify({"error": "Invalid driver_token, length must be between 20 and 80 characters"}), 400

    allowed_characters = re.compile(r'^[A-Za-z0-9\-._~]+$')
    if not allowed_characters.match(driver_token):
        return jsonify({"error": "Invalid driver_token, contains disallowed characters"}), 400

    # Produce message to Kafka
    producer = KafkaProducerService("localhost:9092", "charging_sessions")
    producer.publish_message(key=station_id.encode('utf-8'), value=data)

    return jsonify({"status": "processing"}), 202


# Register blueprint
app.register_blueprint(main_blueprint)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

