import unittest
import json
from unittest.mock import patch, MagicMock
from app import app, add_rating, update_rating, delete_rating, get_rating

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch('app.collection')
    @patch('app.add_rating', return_value='60458fb603c395f9a81c9f4a')
    @patch('app.requests.post')
    def test_add_review(self, mock_post, mock_add_rating, mock_collection):
        post_id = '12345'
        data = {'rating': 4, 'review': 'Great post!'}
        headers = {'user-id': 'user456'}

        inserted_review = MagicMock(inserted_id='60458fb603c395f9a81c9f4b')
        mock_collection.insert_one.return_value = inserted_review
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {'rating_id': '60458fb603c395f9a81c9f4a'}

        response = self.app.post(f'/posts/{post_id}/reviews', data=json.dumps(data), headers=headers, content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 201)
        self.assertIn('review_id', data)
        self.assertIn('rating_id', data)

    @patch('app.collection')
    @patch('app.get_rating', return_value={'rating': 4})
    @patch('app.requests.get')
    def test_get_reviews(self, mock_get, mock_get_rating, mock_collection):
        post_id = '12345'
        mock_cursor = MagicMock()
        mock_cursor.__iter__.return_value = [
            {'_id': '60458fb603c395f9a81c9f4b', 'review': 'Great post!', 'user_id': 'user123'}
        ]
        mock_collection.find.return_value = mock_cursor
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'rating': 4}

        response = self.app.get(f'/posts/{post_id}/reviews')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['reviews']), 1)
        self.assertEqual(data['reviews'][0]['review'], 'Great post!')
        self.assertIn('rating', data['reviews'][0])

    @patch('app.collection')
    @patch('app.get_rating', return_value={'rating': 4})
    @patch('app.requests.get')
    def test_get_review(self, mock_get, mock_get_rating, mock_collection):
        post_id = '12345'
        review_id = '60458fb603c395f9a81c9f4b'
        mock_collection.find_one.return_value = {
            '_id': '60458fb603c395f9a81c9f4b', 'review': 'Great post!', 'user_id': 'user123'
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'rating': 4}

        response = self.app.get(f'/posts/{post_id}/reviews/{review_id}')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['review']['review'], 'Great post!')
        self.assertIn('rating', data['review'])

    @patch('app.collection')
    @patch('app.update_rating', return_value=4)
    @patch('app.requests.put')
    def test_update_review(self, mock_put, mock_update_rating, mock_collection):
        post_id = '12345'
        review_id = '60458fb603c395f9a81c9f4b'
        data = {'review': 'Updated review', 'rating': 5}

        mock_collection.find_one_and_update.return_value = {
            '_id': '60458fb603c395f9a81c9f4b', 'review': 'Updated review', 'user_id': 'user123'
        }
        mock_put.return_value.status_code = 200
        mock_put.return_value.json.return_value = {'review': 'Updated review', 'rating': 5}

        response = self.app.put(f'/posts/{post_id}/reviews/{review_id}', data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['review']['review'], 'Updated review')
        self.assertIn('rating', data['review'])

    @patch('app.collection')
    @patch('app.requests.put')
    def test_update_nonexistent_review(self, mock_put, mock_collection):
        post_id = '12345'
        review_id = '60458fb603c395f9a81c9f4b'
        data = {'review': 'Updated review', 'rating': 5}
        mock_collection.find_one_and_update.return_value = None
        mock_put.return_value.status_code = 404

        response = self.app.put(f'/posts/{post_id}/reviews/{review_id}', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 404)

    @patch('app.collection')
    @patch('app.delete_rating', return_value=0)
    @patch('app.requests.delete')
    def test_delete_review(self, mock_delete, mock_delete_rating, mock_collection):
        post_id = '12345'
        review_id = '60458fb603c395f9a81c9f4b'
        mock_result = MagicMock(deleted_count=1)
        mock_collection.delete_one.return_value = mock_result
        mock_delete.return_value.status_code = 200

        response = self.app.delete(f'/posts/{post_id}/reviews/{review_id}')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['deleted'], 1)

    @patch('app.collection')
    @patch('app.delete_rating', return_value=None)
    @patch('app.requests.delete')
    def test_delete_review_error(self, mock_delete, mock_delete_rating, mock_collection):
        post_id = '12345'
        review_id = '60458fb603c395f9a81c9f4b'
        mock_result = MagicMock(deleted_count=1)
        mock_collection.delete_one.return_value = mock_result
        mock_delete.return_value.status_code = 500

        response = self.app.delete(f'/posts/{post_id}/reviews/{review_id}')
        data = response.data.decode('utf-8')

        self.assertEqual(response.status_code, 500)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()

