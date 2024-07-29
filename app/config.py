import os


class Config:
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'charging_sessions')
    AUTHORIZATION_SERVICE_URL = os.getenv('AUTHORIZATION_SERVICE_URL', 'http://127.0.0.1:5000/check')
