from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://mongodb:27017/')
db = client['blog']
collection = db['ratings']

@app.route('/posts/<int:post_id>/ratings', methods=['POST'])
def add_rating(post_id):
    data = request.get_json()
    rating = data.get('rating')
    collection.update_one({'post_id': post_id}, {'$set': {'rating': rating}}, upsert=True)
    return jsonify({'success': True}), 201

@app.route('/posts/<int:post_id>/ratings', methods=['GET'])
def get_rating(post_id):
    rating = collection.find_one({'post_id': post_id}, {'_id': 0, 'rating': 1})
    if rating:
        return jsonify({'rating': rating['rating']})
    else:
        return jsonify({'error': 'Rating not found'}), 404

@app.route('/posts/<int:post_id>/ratings', methods=['DELETE'])
def delete_rating(post_id):
    result = collection.delete_one({'post_id': post_id})
    if result.deleted_count > 0:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Rating not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

