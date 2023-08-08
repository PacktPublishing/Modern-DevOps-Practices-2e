import unittest
import json
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.collection')
    def test_get_all_posts(self, mock_collection):
        mock_cursor = MagicMock()
        mock_cursor.__iter__.return_value = [
            {'_id': '60458fb603c395f9a81c9f4a', 'title': 'Test Title', 'content': 'Test Content', 'user_id': 'user123'}
        ]
        mock_collection.find.return_value = mock_cursor

        response = self.app.get('/posts')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Title')
        self.assertEqual(data[0]['content'], 'Test Content')
        self.assertEqual(data[0]['user_id'], 'user123')

    @patch('app.collection')
    def test_create_post(self, mock_collection):
        new_post = {'title': 'New Title', 'content': 'New Content'}
        headers = {'user-id': 'user456'}

        inserted_post = {'_id': '60458fb603c395f9a81c9f4a'}
        mock_collection.insert_one.return_value = MagicMock(inserted_id='60458fb603c395f9a81c9f4a')

        response = self.app.post('/posts', data=json.dumps(new_post), headers=headers, content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertIn('post', data)

    @patch('app.collection')
    def test_get_post(self, mock_collection):
        mock_collection.find_one.return_value = {
            '_id': '60458fb603c395f9a81c9f4a', 'title': 'Test Title', 'content': 'Test Content', 'user_id': 'user789'
        }
        response = self.app.get('/posts/60458fb603c395f9a81c9f4a')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['post']['title'], 'Test Title')
        self.assertEqual(data['post']['content'], 'Test Content')
        self.assertEqual(data['post']['user_id'], 'user789')

    @patch('app.collection')
    def test_get_nonexistent_post(self, mock_collection):
        mock_collection.find_one.return_value = None
        response = self.app.get('/posts/60458fb603c395f9a81c9f4a')

        self.assertEqual(response.status_code, 404)

    @patch('app.collection')
    def test_update_post(self, mock_collection):
        updated_post = {'title': 'Updated Title', 'content': 'Updated Content'}
        mock_collection.find_one_and_update.return_value = {
            '_id': '60458fb603c395f9a81c9f4a', 'title': 'Updated Title', 'content': 'Updated Content', 'user_id': 'user012'
        }
        response = self.app.put('/posts/60458fb603c395f9a81c9f4a', data=json.dumps(updated_post), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['post']['title'], 'Updated Title')
        self.assertEqual(data['post']['content'], 'Updated Content')

    @patch('app.collection')
    def test_update_nonexistent_post(self, mock_collection):
        mock_collection.find_one_and_update.return_value = None
        response = self.app.put('/posts/60458fb603c395f9a81c9f4a', data=json.dumps({}), content_type='application/json')

        self.assertEqual(response.status_code, 404)

    @patch('app.collection')
    def test_delete_post(self, mock_collection):
        mock_result = MagicMock(deleted_count=1)
        mock_collection.delete_one.return_value = mock_result

        response = self.app.delete('/posts/60458fb603c395f9a81c9f4a')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['deleted'], 1)

    @patch('app.collection')
    def test_delete_nonexistent_post(self, mock_collection):
        mock_result = MagicMock(deleted_count=0)
        mock_collection.delete_one.return_value = mock_result

        response = self.app.delete('/posts/60458fb603c395f9a81c9f4a')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['deleted'], 0)

if __name__ == '__main__':
    unittest.main()

