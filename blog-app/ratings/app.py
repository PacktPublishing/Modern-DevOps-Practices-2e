from flask import Flask, request, jsonify
from pymongo import MongoClient
import urllib.parse
import os

app = Flask(__name__)
username = os.environ.get('MONGODB_USERNAME')
password = os.environ.get('MONGODB_PASSWORD')
client = MongoClient(f'mongodb://{username}:{urllib.parse.quote_plus(str(password))}@mongodb:27017/')
db = client['blog']
collection = db['ratings']


@app.route('/review/<review_id>/rating/<int:rating>', methods=['POST'])
def add_rating(review_id, rating):
    inserted_rating = collection.insert_one(
        {'review_id': review_id, 'rating': rating})
    return jsonify({'rating_id': str(inserted_rating.inserted_id)}), 201


@app.route('/review/<review_id>/rating', methods=['GET'])
def get_rating(review_id):
    rating = collection.find_one({'review_id': review_id})
    if rating:
        return jsonify({'rating': rating['rating'], 'color': 'orange'})
    else:
        return jsonify({'error': 'Rating not found'}), 404


@app.route('/review/<review_id>/rating/<int:rating>', methods=['PUT'])
def update_rating(review_id, rating):
    rating = collection.find_one_and_update(
        {'review_id': review_id}, {'$set': {'rating': rating}}, return_document=True)
    if rating:
        return jsonify({'rating': rating['rating']})
    else:
        return jsonify({'error': 'Rating not found'}), 404


@app.route('/review/<review_id>/rating', methods=['DELETE'])
def delete_rating(review_id):
    result = collection.delete_one({'review_id': review_id})
    return jsonify({'deleted': result.deleted_count})


if __name__ == '__main__':
    app.run(debug=True)
