from kafka import KafkaProducer
import json


class KafkaProducerService:
    def __init__(self, servers, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def publish_message(self, key, value):
        self.producer.send(self.topic, key=key, value=value)
