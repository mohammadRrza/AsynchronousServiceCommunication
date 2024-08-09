import os
import sys

import pytest
import json
from uuid import uuid4

# Get the absolute path of the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the project's root directory to Python's PATH
sys.path.insert(0, project_root)

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_start_session_invalid_json(client):
    response = client.post('/api/start_session', data="not a json")
    assert response.status_code == 400
    assert response.json == {"error": "Invalid request format, JSON expected"}


def test_start_session_invalid_station_id(client):
    payload = {
        "station_id": "invalid-uuid",
        "driver_token": "validDriverToken12345"
    }
    response = client.post('/api/start_session', json=payload)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid station_id, must be a valid UUIDv4"}


def test_start_session_invalid_driver_token_length(client):
    payload = {
        "station_id": str(uuid4()),
        "driver_token": "short"
    }
    response = client.post('/api/start_session', json=payload)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid driver_token, length must be between 20 and 80 characters"}


def test_start_session_invalid_driver_token_characters(client):
    payload = {
        "station_id": str(uuid4()),
        "driver_token": "invalid$character!"
    }
    response = client.post('/api/start_session', json=payload)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid driver_token, contains disallowed characters"}


def test_start_session_success(client, mocker):
    payload = {
        "station_id": str(uuid4()),
        "driver_token": "validDriverToken12345"
    }

    # Mock KafkaProducerService to prevent actual Kafka interaction
    mock_producer = mocker.Mock()
    mocker.patch('app.KafkaProducerService', return_value=mock_producer)

    response = client.post('/api/start_session', json=payload)
    assert response.status_code == 202
    assert response.json == {"status": "processing"}

    # Ensure the publish_message method was called with correct parameters
    mock_producer.publish_message.assert_called_once_with(
        key=payload['station_id'].encode('utf-8'),
        value=payload
    )
