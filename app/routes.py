from flask import Flask, Blueprint, request, jsonify
from kafka import KafkaProducer
import json
import logging

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
        print("salalalalaalal")
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
@main_blueprint.route('/api/start_session', methods=['POST'])
def start_session():
    data = request.json
    if not data or 'station_id' not in data or 'driver_token' not in data:
        return jsonify({"error": "Invalid data"}), 400

    station_id = data.get('station_id')
    driver_token = data.get('driver_token')

    producer = KafkaProducerService("localhost:9092", "charging_sessions")
    producer.publish_message(key=station_id.encode('utf-8'), value=data)

    return jsonify({"status": "processing"}), 202


# Register blueprint
app.register_blueprint(main_blueprint)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

