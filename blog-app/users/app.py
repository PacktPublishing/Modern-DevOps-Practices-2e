from flask import Flask, request, jsonify
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib.parse
import os

app = Flask(__name__)
username = os.environ.get('MONGODB_USERNAME')
password = os.environ.get('MONGODB_PASSWORD')
client = MongoClient(f'mongodb://{username}:{urllib.parse.quote_plus(str(password))}@mongodb:27017/')
db = client['blog']
collection = db['users']


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = collection.find_one({'_id': user_id})
    if user:
        return jsonify({'user': user})
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')
    try:
        user = {'firstname': firstname, 'lastname': lastname,
                '_id': email, 'password': password}
        inserted_user = collection.insert_one(user)
        return jsonify({'user': str(inserted_user.inserted_id)}), 201
    except pymongo.errors.DuplicateKeyError:
        return jsonify({'error': 'User already exists'}), 409


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    password = data.get('password')
    user = collection.find_one_and_update({'_id': user_id}, {'$set': {
                                          'firstname': firstname, 'lastname': lastname, 'password': password}}, return_document=True)
    if user:
        user['_id'] = str(user['_id'])
        return jsonify({'user': user})
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = collection.delete_one({'_id': user_id})
    return jsonify({'deleted': result.deleted_count})


if __name__ == '__main__':
    app.run(debug=True)
