import unittest
from unittest.mock import patch, MagicMock
import asynctest
from aioresponses import aioresponses
from aiokafka import AIOKafkaConsumer
import json
import asyncio
import sys
import os

# Get the absolute path of the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project's root directory to Python's PATH
sys.path.insert(0, project_root)
from consumer.consumer import AsyncKafkaConsumerService  # Import the service to be tested


class TestAsyncKafkaConsumerService(asynctest.TestCase):
    def setUp(self):
        # Method for initializing the consumer service
        self.servers = ['localhost:9092']
        self.topic = 'charging_sessions'
        self.group_id = 'auth-group'
        self.auth_service_url = 'http://127.0.0.1:5000/check'
        self.consumer = AsyncKafkaConsumerService(
            servers=self.servers,
            topic=self.topic,
            group_id=self.group_id,
            auth_service_url=self.auth_service_url
        )

    @patch('aiokafka.AIOKafkaConsumer')  # The AIOKafkaConsumer Mock Test for start process
    async def test_start_consumer(self, MockAIOKafkaConsumer):
        # Mock the behavior of the Kafka consumer
        mock_consumer = MockAIOKafkaConsumer.return_value
        mock_consumer.start = asynctest.CoroutineMock()
        mock_consumer.stop = asynctest.CoroutineMock()
        # Simulate receiving a message from Kafka
        mock_consumer.__aiter__.return_value = [MagicMock(value=json.dumps({
            'station_id': '123e4567-e89b-12d3-a456-426614174000',
            'driver_token': 'validDriverToken12345'
        }).encode('utf-8'))]

        with aioresponses() as m:
            # The HTTP POST request Mock test for auth service
            m.post(self.auth_service_url, payload={'status': 'active'}, status=200)

            # Running the consumer and checking its behavior
            await self.consumer.start_consumer()

        # Ensure that the consumer's start and stop methods were called once
        mock_consumer.start.assert_called_once()
        mock_consumer.stop.assert_called_once()

    @patch('aiokafka.AIOKafkaConsumer')  # The AIOKafkaConsumer Mock Test for checking if message is successful
    async def test_process_message_successful(self, MockAIOKafkaConsumer):
        # Test the process_message method when HTTP request is successful
        data = {
            'station_id': '123e4567-e89b-12d3-a456-426614174000',
            'driver_token': 'validDriverToken12345'
        }
        message = MagicMock(value=json.dumps(data).encode('utf-8'))

        with aioresponses() as m:
            # Mock the HTTP POST request to the auth service
            m.post(self.auth_service_url, payload={'status': 'active'}, status=200)

            # Call process_message and check its behavior
            await self.consumer.process_message(data)

    @patch('aiokafka.AIOKafkaConsumer')  # Mock the AIOKafkaConsumer
    async def test_process_message_timeout(self, MockAIOKafkaConsumer):
        # Test the process_message method when HTTP request times out
        data = {
            'station_id': '123e4567-e89b-12d3-a456-426614174000',
            'driver_token': 'validDriverToken12345'
        }
        with aioresponses() as m:
            # Simulate a timeout error for the HTTP request
            m.post(self.auth_service_url, exception=asyncio.TimeoutError)

            # Call process_message and check its behavior
            await self.consumer.process_message(data)

    @patch('aiokafka.AIOKafkaConsumer')  # Mock the AIOKafkaConsumer
    async def test_process_message_http_error(self, MockAIOKafkaConsumer):
        # Test the process_message method when HTTP request returns an error status
        data = {
            'station_id': '123e4567-e89b-12d3-a456-426614174000',
            'driver_token': 'validDriverToken12345'
        }
        with aioresponses() as m:
            # Mock the HTTP POST request to return a 500 error
            m.post(self.auth_service_url, status=500)

            # Call process_message and check its behavior
            await self.consumer.process_message(data)

    @patch('aiokafka.AIOKafkaConsumer')  # Mock the AIOKafkaConsumer
    async def test_process_message_json_decode_error(self, MockAIOKafkaConsumer):
        # Test the process_message method when HTTP response contains invalid JSON
        data = {
            'station_id': '123e4567-e89b-12d3-a456-426614174000',
            'driver_token': 'validDriverToken12345'
        }
        with aioresponses() as m:
            # Mock the HTTP POST request to return invalid JSON
            m.post(self.auth_service_url, body='invalid json', status=200)

            # Call process_message and check its behavior
            await self.consumer.process_message(data)


if __name__ == "__main__":
    unittest.main()
