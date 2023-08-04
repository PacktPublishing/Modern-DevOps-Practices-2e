from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
posts_service_url = 'http://posts:5000'
reviews_service_url = 'http://reviews:5000'
ratings_service_url = 'http://ratings:5000'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def get_all_posts():
    response = requests.get(f'{posts_service_url}/posts')
    posts = response.json()
    return render_template('posts.html', posts=posts)

@app.route('/posts/<post_id>')
def get_post(post_id):
    response = requests.get(f'{posts_service_url}/posts/{post_id}')
    post = response.json().get('post')
    if post:
        review_response = requests.get(f'{reviews_service_url}/posts/{post_id}/reviews')
        reviews = review_response.json().get('reviews', [])
        return render_template('post.html', post=post, reviews=reviews)
    else:
        return render_template('error.html', message='Post not found'), 404

@app.route('/posts/<post_id>/update')
def update_post_redirect(post_id):
    response = requests.get(f'{posts_service_url}/posts/{post_id}')
    post = response.json().get('post')
    if post:
        review_response = requests.get(f'{reviews_service_url}/posts/{post_id}/reviews')
        return render_template('add_or_update_post.html', post=post)
    else:
        return render_template('error.html', message='Post not found'), 404

@app.route('/posts/<post_id>/update', methods=['POST'])
def update_post(post_id):
    title = request.form.get('title')
    content = request.form.get('content')
    requests.put(f'{posts_service_url}/posts/{post_id}', json={'title': title, 'content': content})
    return get_post(post_id)

@app.route('/posts/add')
def add_post_redirect():
    return render_template('add_or_update_post.html')

@app.route('/posts', methods=['POST'])
def add_post():
    title = request.form.get('title')
    content = request.form.get('content')
    response = requests.post(f'{posts_service_url}/posts', json={'title': title, 'content': content})
    return get_post(response.json().get("post"))

@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    requests.delete(f'{posts_service_url}/posts/{post_id}')
    return get_all_posts()

@app.route('/posts/<post_id>/reviews', methods=['POST'])
def add_review(post_id):
    review = request.form.get('review')
    rating = request.form.get('rating')
    requests.post(f'{reviews_service_url}/posts/{post_id}/reviews', json={'review': review, 'rating': rating})
    return get_post(post_id)

@app.route('/posts/<post_id>/reviews/<review_id>', methods=['POST'])
def update_review(post_id, review_id):
    review = request.form.get('review')
    rating = request.form.get('rating')
    requests.put(f'{reviews_service_url}/posts/{post_id}/reviews/{review_id}', json={'review': review, 'rating': rating})
    return get_post(post_id)

@app.route('/posts/<post_id>/reviews/<review_id>')
def update_or_delete_review(post_id, review_id):
    action = request.args.get('action')
    if action == "delete":
        requests.delete(f'{reviews_service_url}/posts/{post_id}/reviews/{review_id}')
        return get_post(post_id)
    elif action == "update":
        response = requests.get(f'{posts_service_url}/posts/{post_id}')
        post = response.json().get('post')
        if post:
            review_response = requests.get(f'{reviews_service_url}/posts/{post_id}/reviews/{review_id}')
            review = review_response.json().get('review', {})
            return render_template('update_review.html', post=post, review=review)
        else:
            return render_template('error.html', message='Review not found'), 404

if __name__ == '__main__':
    app.run(debug=True)

