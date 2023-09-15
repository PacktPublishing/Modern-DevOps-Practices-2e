from flask import Flask, render_template, request, jsonify, session
import requests
import base64
from flask_session import Session
from flask_bcrypt import Bcrypt

app = Flask(__name__)
posts_service_url = 'http://posts:5000'
reviews_service_url = 'http://reviews:5000'
ratings_service_url = 'http://ratings:5000'
users_service_url = 'http://users:5000'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    response = requests.get(f'{posts_service_url}/posts')
    posts = response.json()
    return render_template('index.html', posts=posts)


def error_message(message):
    response = requests.get(f'{posts_service_url}/posts')
    posts = response.json()
    return render_template('index.html', posts=posts, error_message=message)

@app.errorhandler(Exception)
def handle_global_error(e):
    return error_message(repr(e))

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form.get("email")
    password = request.form.get("password")
    # Get the credentials from the users service
    response = requests.get(f'{users_service_url}/users/{user_id}')
    user = response.json().get('user')
    if not user:
        return error_message("User not found")
    actual_password = user["password"]
    password_matched = bcrypt.check_password_hash(actual_password, password)
    if not password_matched:
        return error_message("Incorrect Password")
    # Set the session variable
    user.pop('password')
    session["user"] = user
    return index()


@app.route('/logout')
def logout():
    session["user"] = None
    return index()


@app.route('/register', methods=['POST'])
def register():
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    password = bcrypt.generate_password_hash(
        request.form.get("password")).decode('utf-8')
    # Create a user using the users service
    response = requests.post(f'{users_service_url}/users', json={
                             'firstname': firstname, 'lastname': lastname, 'email': email, 'password': password})
    # Get the credentials from the users service
    response = requests.get(f'{users_service_url}/users/{email}')
    user = response.json().get('user')
    if not user:
        return error_message("User not found")
    # Set the session variable
    user.pop('password')
    session["user"] = user
    return index()


@app.route('/updateprofile', methods=['POST'])
def update_profile():
    user_id = session["user"]["_id"]
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    password = request.form.get("password")
    # Update a user using the users service
    response = requests.put(f'{users_service_url}/users/{user_id}', json={
                            'firstname': firstname, 'lastname': lastname, 'password': password})
    # Get the credentials from the users service
    response = requests.get(f'{users_service_url}/users/{email}')
    user = response.json().get('user')
    if not user:
        return error_message("User not found")
    # Set the session variable
    user.pop('password')
    session["user"] = user
    return index()

@app.route('/deleteprofile', methods=['POST'])
def delete_profile():
    user_id = session["user"]["_id"]
    # Delete the user
    print('user_id', user_id, flush=True)
    response = requests.delete(f'{users_service_url}/users/{user_id}')
    print('response', response, flush=True)
    return logout()


@app.route('/posts/<post_id>')
def get_post(post_id):
    response = requests.get(f'{posts_service_url}/posts/{post_id}')
    post = response.json().get('post')
    if post:
        review_response = requests.get(
            f'{reviews_service_url}/posts/{post_id}/reviews')
        reviews = review_response.json().get('reviews', [])
        return render_template('index.html', post=post, reviews=reviews)
    else:
        return error_message('Post not found')


@app.route('/posts/<post_id>/update')
def update_post_redirect(post_id):
    response = requests.get(f'{posts_service_url}/posts/{post_id}')
    post = response.json().get('post')
    if post:
        return render_template('post.html', post=post)
    else:
        return error_message('Post not found')


@app.route('/posts/<post_id>/update', methods=['POST'])
def update_post(post_id):
    title = request.form.get('title')
    content = request.form.get('content')
    requests.put(f'{posts_service_url}/posts/{post_id}',
                 json={'title': title, 'content': content})
    return get_post(post_id)


@app.route('/posts/add')
def add_post_redirect():
    return render_template('post.html')


@app.route('/posts', methods=['POST'])
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    user_id = session["user"]["_id"]
    headers = {"user-id": user_id}
    response = requests.post(f'{posts_service_url}/posts',
                             headers=headers, json={'title': title, 'content': content})
    return get_post(response.json().get("post"))


@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    requests.delete(f'{posts_service_url}/posts/{post_id}')
    return index()


@app.route('/posts/<post_id>/reviews', methods=['POST'])
def add_review(post_id):
    review = request.form.get('review')
    rating = request.form.get('rating')
    user_id = session["user"]["_id"]
    headers = {"user-id": user_id}
    requests.post(f'{reviews_service_url}/posts/{post_id}/reviews',
                  headers=headers, json={'review': review, 'rating': rating})
    return get_post(post_id)


@app.route('/posts/<post_id>/reviews/<review_id>', methods=['POST'])
def update_review(post_id, review_id):
    review = request.form.get('review')
    rating = request.form.get('rating')
    requests.put(f'{reviews_service_url}/posts/{post_id}/reviews/{review_id}',
                 json={'review': review, 'rating': rating})
    return get_post(post_id)


@app.route('/posts/<post_id>/reviews/<review_id>')
def update_or_delete_review(post_id, review_id):
    action = request.args.get('action')
    if action == "delete":
        requests.delete(
            f'{reviews_service_url}/posts/{post_id}/reviews/{review_id}')
        return get_post(post_id)
    elif action == "update":
        response = requests.get(f'{posts_service_url}/posts/{post_id}')
        post = response.json().get('post')
        if post:
            review_response = requests.get(
                f'{reviews_service_url}/posts/{post_id}/reviews/{review_id}')
            review = review_response.json().get('review', {})
            return render_template('index.html', post=post, review=review)
        else:
            return error_message('Review not found')


if __name__ == '__main__':
    app.run(debug=True)
