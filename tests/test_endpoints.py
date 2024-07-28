import unittest
from app import create_app


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_start_session(self):
        response = self.client.post('/api/start_session', json={
            'station_id': '123e4567-e89b-12d3-a456-426614174000',
            'driver_token': 'validDriverToken12345'
        })
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json['status'], 'processing')


if __name__ == '__main__':
    unittest.main()
