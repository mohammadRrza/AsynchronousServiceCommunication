import asyncio
from aiokafka import AIOKafkaConsumer
import aiohttp
import json
import logging


class AsyncKafkaConsumerService:
    def __init__(self, servers, topic, group_id, auth_service_url):
        self.servers = servers
        self.topic = topic
        self.group_id = group_id
        self.auth_service_url = auth_service_url
        self.consumer = None
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def start_consumer(self):
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.servers,
            group_id=self.group_id,
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        await self.consumer.start()
        self.logger.info("Starting to consume messages from topic.")

        try:
            async for message in self.consumer:
                await self.process_message(message.value)
        finally:
            await self.consumer.stop()

    async def process_message(self, data):
        self.logger.info(f"Received message: {data}")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.auth_service_url, json=data) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        self.logger.info(f"Driver Token Status: {response_data['status']}")
                        self.logger.info("Message processed successfully.")
                    else:
                        self.logger.error(f"Error processing message: {response.status}")
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to decode JSON response: {e}")
            except aiohttp.ClientError as e:
                self.logger.error(f"Request failed: {e}")


async def main():
    consumer = AsyncKafkaConsumerService(
        servers=['localhost:9092'],
        topic='charging_sessions',
        group_id='auth-group',
        auth_service_url='http://127.0.0.1:5000/check'
    )
    await consumer.start_consumer()


if __name__ == "__main__":
    asyncio.run(main())
