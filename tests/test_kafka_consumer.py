import unittest
from unittest.mock import patch, MagicMock
import asynctest
from aioresponses import aioresponses
from aiokafka import AIOKafkaConsumer
import json
import asyncio
from consumer.consumer import AsyncKafkaConsumerService 



class TestAsyncKafkaConsumerService(asynctest.TestCase):
    def setUp(self):
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

    @patch('aiokafka.AIOKafkaConsumer')
    async def test_start_consumer(self, MockAIOKafkaConsumer):
        mock_consumer = MockAIOKafkaConsumer.return_value
        mock_consumer.start = asynctest.CoroutineMock()
        mock_consumer.stop = asynctest.CoroutineMock()
        mock_consumer.__aiter__.return_value = [MagicMock(value=json.dumps({'key': 'value'}).encode('utf-8'))]

        with aioresponses() as m:
            m.post(self.auth_service_url, payload={'status': 'active'}, status=200)

            await self.consumer.start_consumer()

        mock_consumer.start.assert_called_once()
        mock_consumer.stop.assert_called_once()

    @patch('aiokafka.AIOKafkaConsumer')
    async def test_process_message_successful(self, MockAIOKafkaConsumer):
        data = {'key': 'value'}
        message = MagicMock(value=json.dumps(data).encode('utf-8'))
        
        with aioresponses() as m:
            m.post(self.auth_service_url, payload={'status': 'active'}, status=200)

            await self.consumer.process_message(data)

    @patch('aiokafka.AIOKafkaConsumer')
    async def test_process_message_timeout(self, MockAIOKafkaConsumer):
        data = {'key': 'value'}
        
        with aioresponses() as m:
            m.post(self.auth_service_url, exception=asyncio.TimeoutError)

            await self.consumer.process_message(data)

    @patch('aiokafka.AIOKafkaConsumer')
    async def test_process_message_http_error(self, MockAIOKafkaConsumer):
        data = {'key': 'value'}
        
        with aioresponses() as m:
            m.post(self.auth_service_url, status=500)

            await self.consumer.process_message(data)

    @patch('aiokafka.AIOKafkaConsumer')
    async def test_process_message_json_decode_error(self, MockAIOKafkaConsumer):
        data = {'key': 'value'}
        
        with aioresponses() as m:
            m.post(self.auth_service_url, body='invalid json', status=200)

            await self.consumer.process_message(data)


if __name__ == "__main__":
    unittest.main()
