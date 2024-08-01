# AsynchronousServiceCommunication

## Project Overview
**AsynchronousServiceCommunication** is a project designed to facilitate communication between services in an asynchronous manner. This project aims to improve the scalability and responsiveness of service interactions by leveraging asynchronous messaging patterns.

## Features
- **Asynchronous Messaging:** Efficiently handle inter-service communication without blocking.
- **Scalability:** Designed to scale with increased service load and message volume.
- **Reliability:** Ensures message delivery and handling even under failure conditions.
- **Extensibility:** Easily extendable to support various messaging protocols and patterns.

## Getting Started

### Prerequisites
- Python 3.x (if running locally)
- Necessary Python packages (listed in `requirements.txt`)
- Message broker (Kafka)

Certainly! You can add detailed instructions on how to install and run Kafka in the README.md. Here’s a revised version of the Installation section with added Kafka setup instructions:


# AsynchronousServiceCommunication

## Project Overview
**AsynchronousServiceCommunication** is a project designed to facilitate communication between services in an asynchronous manner. The goal is to enhance scalability and responsiveness of service interactions by leveraging asynchronous messaging patterns.

## Features
- **Asynchronous Messaging:** Efficiently handles inter-service communication without blocking.
- **Scalability:** Designed to scale with increased service load and message volume.
- **Reliability:** Ensures message delivery and handling even under failure conditions.
- **Extensibility:** Easily extendable to support various messaging protocols and patterns.

## Getting Started

### Prerequisites
- Python 3.x (if running locally)
- Necessary Python packages (listed in `requirements.txt`)
- Kafka (for message brokering)

### Installation

#### Running Locally

1. **Clone the repository:**
    ```bash
    git clone https://github.com/mohammadRrza/AsynchronousServiceCommunication.git
    cd AsynchronousServiceCommunication
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

#### Installing and Running Kafka

1. **Download Kafka:**
   - Go to the [Apache Kafka Downloads page](https://kafka.apache.org/downloads) and download the latest binary release of Kafka.

2. **Extract the Kafka archive:**
    ```bash
    tar -xzf kafka_2.12.3.8.0.tgz  
    cd kafka_2.12.3.8.0
    ```

3. **Start Zookeeper:**
   Kafka requires Zookeeper to manage its cluster. In a new terminal, start Zookeeper with the following command:
    ```bash
    bin/zookeeper-server-start.sh config/zookeeper.properties
    ```

4. **Start Kafka:**
   In another new terminal, start Kafka with the following command:
    ```bash
    bin/kafka-server-start.sh config/server.properties
    ```

5. **Create a Kafka Topic (optional):**
   To create a topic for testing or production use, run:
    ```bash
    bin/kafka-topics.sh --create --topic your_topic_name --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
    ```
   Replace `your_topic_name` with the name of your topic.

### Configuration
1. **Update Configuration Files:**
   - Configure Kafka and other settings in the `config` directory.
   - Modify configuration files to include the correct Kafka broker addresses and other necessary parameters.
   - Configure the message broker(Kafka) and other settings in the `config` directory. Ensure you update the configuration files with the correct settings for your environment.


### Usage
1. Start the service:
    ```bash
    flask run
    ```
2. To test the service, you can use the provided test scripts in the `tests` directory.

### Running the Tests
1. Start the service:
    ```bash
    pytest tests
    ```

### Running python consumer package
1. Start the consumer package:
    ```bash
    python3 consumer/consumer.py
    ```
**you can read a complete document about consumer [here](https://github.com/mohammadRrza/AsynchronousServiceCommunication/blob/main/consumer/docs/consumer_doc.md)
   
## Contributing
1. Fork the repository.
2. Create a new feature branch.
3. FCommit your changes.
4. Push the branch and create a pull request.


## Contact

For any questions or inquiries, please contact [Mohammad Reza](mr.taheri25461@gmail.com).
