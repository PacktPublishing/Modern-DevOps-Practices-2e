from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
import urllib.parse
import os

app = Flask(__name__)
username = os.environ.get('MONGODB_USERNAME')
password = os.environ.get('MONGODB_PASSWORD')
client = MongoClient(f'mongodb://{username}:{urllib.parse.quote_plus(str(password))}@mongodb:27017/')
db = client['blog']
collection = db['reviews']
ratings_service_url = 'http://ratings:5000'


def add_rating(review_id, rating):
    try:
        res = requests.post(
            f'{ratings_service_url}/review/{review_id}/rating/{rating}')
        if res.status_code == 201:
            return res.json()['rating_id']
    except Exception as e:
        print("Exception: ", e, flush=True)
        return None


def update_rating(review_id, rating):
    try:
        res = requests.put(
            f'{ratings_service_url}/review/{review_id}/rating/{rating}')
        if res.status_code == 200:
            return res.json()['rating']
    except Exception as e:
        print("Exception: ", e, flush=True)
        return None


def delete_rating(review_id):
    try:
        res = requests.delete(
            f'{ratings_service_url}/review/{review_id}/rating')
        if res.status_code == 200:
            return 0
    except Exception as e:
        print("Exception: ", e, flush=True)
        return None


def get_rating(review_id):
    try:
        res = requests.get(f'{ratings_service_url}/review/{review_id}/rating')
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        print("Exception: ", e, flush=True)
        return None


@app.route('/posts/<post_id>/reviews', methods=['POST'])
def add_review(post_id):
    data = request.get_json()
    rating = data.get('rating')
    review = data.get('review')
    user_id = request.headers.get('user-id')
    # Insert review here
    inserted_review = collection.insert_one(
        {'post_id': post_id, 'review': review, 'user_id': user_id})
    # Return the id of reviews and ratings if successful
    resp = {}
    if inserted_review:
        resp['review_id'] = str(inserted_review.inserted_id)
        # Call the ratings service to insert ratings
        rating_id = add_rating(inserted_review.inserted_id, rating)
        if rating_id:
            resp['rating_id'] = rating_id
    return jsonify(resp), 201


@app.route('/posts/<post_id>/reviews', methods=['GET'])
def get_reviews(post_id):
    cursor = collection.find({'post_id': post_id})
    reviews = []
    for review in cursor:
        review['_id'] = str(review['_id'])
        # Get rating of the review
        rating = get_rating(review['_id'])
        if rating:
            review['rating'] = rating
        reviews.append(review)
    return jsonify({'reviews': reviews})


@app.route('/posts/<post_id>/reviews/<review_id>', methods=['GET'])
def get_review(post_id, review_id):
    review = collection.find_one({'_id': ObjectId(review_id)})
    if review:
        review['_id'] = str(review['_id'])
        # Get rating of the review
        rating = get_rating(review['_id'])
        if rating:
            review['rating'] = rating
        return jsonify({'review': review})
    else:
        return jsonify({'error': 'Review not found'}), 404


@app.route('/posts/<post_id>/reviews/<review_id>', methods=['PUT'])
def update_review(post_id, review_id):
    data = request.get_json()
    review_content = data.get('review')
    rating = data.get('rating')
    review = collection.find_one_and_update({'_id': ObjectId(review_id)}, {
                                            '$set': {'review': review_content}}, return_document=True)
    # Call the ratings service to update ratings
    rating = update_rating(review_id, rating)
    if review:
        review['_id'] = str(review['_id'])
        if rating:
            review['rating'] = rating
        return jsonify({'review': review})
    else:
        return jsonify({'error': 'Review not found'}), 404


@app.route('/posts/<post_id>/reviews/<review_id>', methods=['DELETE'])
def delete_review(post_id, review_id):
    rating = delete_rating(review_id)
    if rating is None:
        return jsonify({'error': 'Error deleting rating'}), 500
    try:
        result = collection.delete_one({'_id': ObjectId(review_id)})
        return jsonify({'deleted': result.deleted_count})
    except:
        return jsonify({'deleted': 0})


if __name__ == '__main__':
    app.run(debug=True)
