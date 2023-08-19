from flask import Flask, request, jsonify
import urllib.parse
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
username = os.environ.get('MONGODB_USERNAME')
password = os.environ.get('MONGODB_PASSWORD')
client = MongoClient(f'mongodb://{username}:{urllib.parse.quote_plus(str(password))}@mongodb:27017/')
db = client['blog']
collection = db['posts']


@app.route('/posts', methods=['GET'])
def get_all_posts():
    cursor = collection.find()
    posts = []
    for post in cursor:
        post['_id'] = str(post['_id'])
        posts.append(post)
    return jsonify(posts)


@app.route('/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    post = collection.find_one({'_id': ObjectId(post_id)})
    if post:
        post['_id'] = str(post['_id'])
        return jsonify({'post': post})
    else:
        return jsonify({'error': 'Post not found'}), 404


@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = request.headers.get('user-id')
    post = {'title': title, 'content': content, 'user_id': user_id}
    inserted_post = collection.insert_one(post)
    return jsonify({'post': str(inserted_post.inserted_id)}), 201


@app.route('/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    post = collection.find_one_and_update({'_id': ObjectId(post_id)}, {
                                          '$set': {'title': title, 'content': content}}, return_document=True)
    if post:
        post['_id'] = str(post['_id'])
        return jsonify({'post': post})
    else:
        return jsonify({'error': 'Post not found'}), 404


@app.route('/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    result = collection.delete_one({'_id': ObjectId(post_id)})
    return jsonify({'deleted': result.deleted_count})


if __name__ == '__main__':
    app.run(debug=True)
