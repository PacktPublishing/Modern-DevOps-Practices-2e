import unittest
import json
from unittest.mock import patch, MagicMock
import pymongo
from pymongo.errors import DuplicateKeyError
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.collection')
    def test_get_user(self, mock_collection):
        user_id = 'user123'
        mock_collection.find_one.return_value = {
            '_id': user_id, 'firstname': 'John', 'lastname': 'Doe', 'password': 'secret'
        }

        response = self.app.get(f'/users/{user_id}')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['user']['firstname'], 'John')
        self.assertEqual(data['user']['lastname'], 'Doe')
        self.assertEqual(data['user']['password'], 'secret')

    @patch('app.collection')
    def test_update_user(self, mock_collection):
        user_id = 'user123'
        data = {'firstname': 'Jane', 'lastname': 'Doe', 'password': 'newpassword'}
        mock_collection.find_one_and_update.return_value = {
            '_id': user_id, 'firstname': 'Jane', 'lastname': 'Doe', 'password': 'newpassword'
        }

        response = self.app.put(f'/users/{user_id}', data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['user']['firstname'], 'Jane')
        self.assertEqual(data['user']['lastname'], 'Doe')
        self.assertEqual(data['user']['password'], 'newpassword')

    @patch('app.collection')
    def test_update_nonexistent_user(self, mock_collection):
        user_id = 'user123'
        data = {'firstname': 'Jane', 'lastname': 'Doe', 'password': 'newpassword'}
        mock_collection.find_one_and_update.return_value = None

        response = self.app.put(f'/users/{user_id}', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 404)

    @patch('app.collection')
    def test_delete_user(self, mock_collection):
        user_id = 'user123'
        mock_result = MagicMock(deleted_count=1)
        mock_collection.delete_one.return_value = mock_result

        response = self.app.delete(f'/users/{user_id}')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['deleted'], 1)

    @patch('app.collection')
    def test_create_user(self, mock_collection):
        data = {'firstname': 'Alice', 'lastname': 'Smith', 'email': 'alice@example.com', 'password': 'password'}
        mock_collection.insert_one.return_value = MagicMock(inserted_id='user456')

        response = self.app.post('/users', data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['user'], 'user456')

    @patch('app.collection')
    def test_create_existing_user(self, mock_collection):
        data = {'firstname': 'Alice', 'lastname': 'Smith', 'email': 'alice@example.com', 'password': 'password'}
        mock_collection.insert_one.side_effect = DuplicateKeyError("User already exists")

        response = self.app.post('/users', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 409)
        self.assertEqual(json.loads(response.data), {'error': 'User already exists'})

if __name__ == '__main__':
    unittest.main()

