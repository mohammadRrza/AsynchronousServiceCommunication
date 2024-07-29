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
- Docker
- Docker Compose
- Python 3.x (if running locally)
- Necessary Python packages (listed in `requirements.txt`)
- Message broker (Kafka)

Make sure Docker and Docker Compose are installed on your machine. You can download them from the official [Docker website](https://www.docker.com/get-started).
### Installation

#### Using Docker
1. Clone the repository:
    ```bash
    git clone https://github.com/mohammadRrza/AsynchronousServiceCommunication.git
    cd AsynchronousServiceCommunication
    ```
2. Build the Docker image:
    ```bash
    docker-compose build
    ```
3. Start the Services:
    ```bash
    docker-compose up
    ```

4. Stop the Services:
    ```bash
    docker-compose down
    ```
5. Troubleshooting:
    ```bash
    docker-compose logs
    ```
   
#### Running Locally
1. Clone the repository:
    ```bash
    git clone https://github.com/mohammadRrza/AsynchronousServiceCommunication.git
    cd AsynchronousServiceCommunication
    ```
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration
Configure the message broker(Kafka) and other settings in the `config` directory. Ensure you update the configuration files with the correct settings for your environment.

### Usage
1. Start the service:
    ```bash
    python main.py
    ```
2. To test the service, you can use the provided test scripts in the `tests` directory.

### Running the Tests
1. Start the service:
    ```bash
    pytest tests
    ```

## Contributing
1. Fork the repository.
2. Create a new feature branch.
3. FCommit your changes.
4. Push the branch and create a pull request.


## Contact

For any questions or inquiries, please contact [Mohammad Reza](mr.taheri25461@gmail.com).