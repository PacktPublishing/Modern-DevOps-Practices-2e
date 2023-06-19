from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://mongodb:27017/')
db = client['blog']
collection = db['reviews']

@app.route('/posts/<int:post_id>/reviews', methods=['POST'])
def add_review(post_id):
    data = request.get_json()
    rating = data.get('rating')
    review = data.get('review')
    collection.insert_one({'post_id': post_id, 'rating': rating, 'review': review})
    return jsonify({'success': True}), 201

@app.route('/posts/<int:post_id>/reviews', methods=['GET'])
def get_reviews(post_id):
    reviews = list(collection.find({'post_id': post_id}, {'_id': 0}))
    return jsonify({'reviews': reviews})

@app.route('/posts/<int:post_id>/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(post_id, review_id):
    result = collection.delete_one({'post_id': post_id, 'review_id': review_id})
    if result.deleted_count > 0:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Review not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

