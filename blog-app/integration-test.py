import requests
import re

# Define the base URL of your Flask app
BASE_URL = 'http://localhost:8080'  # Update with the correct URL
# Define test data (replace with valid test data)
test_user = {
    'email': 'test@example.com',
    'password': 'password',
    'firstname': 'test',
    'lastname': 'user'
}

updated_test_user = {
    'email': 'test@example.com',
    'password': 'password123',
    'firstname': 'test',
    'lastname': 'user'
}

session = requests.Session()

def test_index():
    response = requests.get(f'{BASE_URL}/')
    assert response.status_code == 200

def test_login(data_val):
    response = session.post(f'{BASE_URL}/login', data=data_val)
    assert '<li><a href="#update-profile-modal">Update Profile</a></li>' in response.text
    assert response.status_code == 200

def test_logout():
    response = session.get(f'{BASE_URL}/logout')
    assert 'href="#login-modal">Sign in</button>' in response.text
    assert response.status_code == 200

def test_register():
    response = requests.post(f'{BASE_URL}/register', data=test_user)
    assert '<li><a href="#update-profile-modal">Update Profile</a></li>' in response.text
    assert response.status_code == 200
    response = session.post(f'{BASE_URL}/updateprofile', data=test_user)

def test_update_profile():
    response = session.post(f'{BASE_URL}/updateprofile', data=updated_test_user)
    assert response.status_code == 200


def test_get_post(post_id):
    response = requests.get(f'{BASE_URL}/posts/{post_id}')
    assert f'<form action="/posts/{post_id}/reviews" method="POST">' in response.text
    assert response.status_code == 200

def test_update_post(post_id):
    response = requests.post(f'{BASE_URL}/posts/{post_id}/update', data={'title': 'Updated Title', 'content': 'Updated Content'})
    assert f'<form action="/posts/{post_id}/reviews" method="POST">' in response.text
    assert 'Updated Title' in response.text
    assert response.status_code == 200

def test_add_post():
    response = session.post(f'{BASE_URL}/posts', data={'title': 'New Post', 'content': 'Post Content'})
    add_post_response = response
    post_id=re.findall("posts.*reviews", add_post_response.text)[0].split('/')[1]
    assert "<h2>New Post</h2>" in add_post_response.text
    assert response.status_code == 200
    if post_id is not None:
        assert f'<form action="/posts/{post_id}/reviews" method="POST">' in add_post_response.text
        return post_id
    else:
        exit(1)

def test_delete_post(post_id):
    response = session.get(f'{BASE_URL}/posts/{post_id}/delete')
    assert "Updated Review" not in response.text
    assert response.status_code == 200

def test_add_review(post_id):
    response = session.post(f'{BASE_URL}/posts/{post_id}/reviews', data={'review': 'Test Review', 'rating': '5'})
    review_post_response = response
    review_id = re.findall("posts.*?action", review_post_response.text)[0].split('/')[3].split('?')[0]
    assert response.status_code == 200
    if review_id is not None:
        assert f'<a href="/posts/{post_id}/reviews/{review_id}?' in review_post_response.text
        return review_id
    else:
        exit(1)

def test_update_review(post_id, review_id):
    response = session.post(f'{BASE_URL}/posts/{post_id}/reviews/{review_id}', data={'review': 'Updated Review', 'rating': '4'})
    assert "Updated Review" in response.text
    assert response.status_code == 200

def test_delete_review(post_id, review_id):
    response = session.get(f'{BASE_URL}/posts/{post_id}/reviews/{review_id}?action=delete')
    assert "posts/{post_id}/reviews/{review_id}" not in response.text
    assert response.status_code == 200

def test_delete_user():
    response = session.post(f'{BASE_URL}/deleteprofile')
    assert response.status_code == 200

if __name__ == '__main__':
    # Run the tests
    post_id = None
    review_id = None
    try:
        test_index()
        test_register()
        test_logout()
        test_login(test_user)
        post_id = test_add_post()
        test_get_post(post_id)
        test_update_post(post_id)
        review_id=test_add_review(post_id)
        test_update_review(post_id, review_id)
        test_update_profile()
    finally:
        if post_id is not None and review_id is not None:
            test_delete_review(post_id, review_id)
        if post_id is not None:
            test_delete_post(post_id)
        if session is not None:
            test_delete_user()
    print("All tests passed!")

