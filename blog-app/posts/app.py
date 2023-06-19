from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://mongodb:27017/')
db = client['blog']
collection = db['posts']

@app.route('/posts', methods=['GET'])
def get_all_posts():
    posts = list(collection.find())
    return jsonify({'posts': posts})

@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = collection.find_one({'id': post_id})
    if post:
        return jsonify({'post': post})
    else:
        return jsonify({'error': 'Post not found'}), 404

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    post_id = collection.count_documents({}) + 1
    post = {'id': post_id, 'title': title, 'content': content}
    collection.insert_one(post)
    return jsonify({'post': post}), 201

@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    post = collection.find_one_and_update({'id': post_id}, {'$set': {'title': title, 'content': content}}, return_document=True)
    if post:
        return jsonify({'post': post})
    else:
        return jsonify({'error': 'Post not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

