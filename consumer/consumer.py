from kafka import KafkaConsumer
import requests
import json
import logging


class KafkaConsumerService:
    def __init__(self, servers, topic, group_id, auth_service_url):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=servers,
            group_id=group_id,
            auto_offset_reset='earliest',  # Ensure this is set
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.auth_service_url = auth_service_url
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def consume_messages(self):
        self.logger.info("Starting to consume messages from topic.")
        for message in self.consumer:
            try:
                data = message.value
                self.logger.info(f"Received message: {data}")

                # Send data to the authentication service
                response = requests.post(self.auth_service_url, json=data)
                if response.status_code == 200:
                    self.logger.info("Message processed successfully.")
                else:
                    self.logger.error(f"Error processing message: {response.text}")
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to decode JSON message: {e}")
            except requests.RequestException as e:
                self.logger.error(f"Request failed: {e}")


if __name__ == "__main__":
    consumer = KafkaConsumerService(
        servers=['localhost:9092'],
        topic='charging_sessions',
        group_id='auth-group',
        auth_service_url='http://auth-service:5000/check'
    )
    consumer.consume_messages()
