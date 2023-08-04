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
    posts = response.json().get('posts', [])
    return render_template('posts.html', posts=posts)

@app.route('/posts/<post_id>')
def get_post(post_id):
    response = requests.get(f'{posts_service_url}/posts/{post_id}')
    post = response.json().get('post')
    if post:
        review_response = requests.get(f'{reviews_service_url}/posts/{post_id}/reviews')
        reviews = review_response.json().get('reviews', [])
        rating_response = requests.get(f'{ratings_service_url}/posts/{post_id}/ratings')
        rating = rating_response.json().get('rating')
        return render_template('post.html', post=post, reviews=reviews, rating=rating)
    else:
        return render_template('error.html', message='Post not found'), 404

@app.route('/posts/<post_id>/reviews', methods=['POST'])
def add_review(post_id):
    review = request.form.get('review')
    rating = request.form.get('rating')
    requests.post(f'{reviews_service_url}/posts/{post_id}/reviews', json={'review': review})
    requests.post(f'{ratings_service_url}/posts/{post_id}/ratings', json={'rating': rating})
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)

