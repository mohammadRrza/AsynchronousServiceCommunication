
# Async Kafka Consumer Service Documentation

## Overview

This document outlines the implementation and usage of an asynchronous Kafka consumer service using `AIOKafkaConsumer` from the `aiokafka` library and `aiohttp` for HTTP requests. This service reads messages from a Kafka topic, processes them, and sends the data to an external authentication service.

## Components

### 1. Imports
- `asyncio`: For asynchronous programming.
- `aiokafka.AIOKafkaConsumer`: To consume messages from Kafka asynchronously.
- `aiohttp`: For making HTTP requests asynchronously.
- `json`: For JSON encoding and decoding.
- `logging`: For logging messages.

### 2. AsyncKafkaConsumerService Class
- **Attributes**:
  - `servers`: Kafka servers (brokers) list.
  - `topic`: The Kafka topic to consume messages from.
  - `group_id`: Consumer group ID.
  - `auth_service_url`: URL for the authentication service.
  - `consumer`: The Kafka consumer instance.
  - `logger`: Logger instance for logging information and errors.

- **Methods**:
  - `__init__(self, servers, topic, group_id, auth_service_url)`: Initializes the service with the given parameters.
  - `setup_logging(self)`: Sets up the logging configuration.
  - `start_consumer(self)`: Starts the Kafka consumer, listens for messages, and processes them.
  - `process_message(self, data)`: Processes each received message by sending it to the authentication service.

### 3. Main Function
- **main()**: Instantiates `AsyncKafkaConsumerService` and starts the consumer.

## Code Explanation

### Initialization

```python
class AsyncKafkaConsumerService:
    def __init__(self, servers, topic, group_id, auth_service_url):
        self.servers = servers
        self.topic = topic
        self.group_id = group_id
        self.auth_service_url = auth_service_url
        self.consumer = None
        self.setup_logging()
```

- Initializes the Kafka consumer service with the provided Kafka servers, topic, consumer group ID, and authentication service URL.
- `setup_logging()` is called to configure logging.

### Logging Setup

```python
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
```

- Configures logging to output messages at the INFO level or higher.
- Creates a logger instance for the service.

### Starting the Consumer

```python
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
```

- Configures the `AIOKafkaConsumer` with the specified topic, servers, group ID, and JSON deserialization.
- Starts the consumer and logs the start message.
- Continuously listens for new messages and processes them using `process_message()`.
- Ensures the consumer stops properly in case of an exception.

### Processing Messages

```python
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
```

- Logs the received message data.
- Sends the message data as a JSON payload to the authentication service.
- Logs the response status and data if successful, or logs an error message otherwise.
- Handles JSON decode errors and HTTP client errors gracefully.

### Main Function

```python
async def main():
    consumer = AsyncKafkaConsumerService(
        servers=['localhost:9092'],
        topic='charging_sessions',
        group_id='auth-group',
        auth_service_url='http://127.0.0.1:5000/check'
    )
    await consumer.start_consumer()
```

- Creates an instance of `AsyncKafkaConsumerService` with specified parameters and starts the consumer.

```python
if __name__ == "__main__":
    asyncio.run(main())
```

- Entry point for running the script, executing the `main()` function in an asyncio event loop.

## Conclusion

This service provides a robust and efficient way to consume Kafka messages asynchronously, process them, and interact with an external API. It includes error handling and logging for better observability and debugging.
