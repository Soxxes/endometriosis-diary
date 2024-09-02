from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from bson.objectid import ObjectId
from backend.extensions import mongo
from backend.models.user import User


users = Blueprint('users', __name__)

@users.route('/add', methods=['POST'])
def add_user():
    data = request.json
    try:
        validated_data, errors = User.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400
        
        user = User(**validated_data)
        user_id = user.save()

        return jsonify({"message": "User added", "id": str(user_id)}), 201
    
    except ValueError as err:
        return jsonify({"errors": str(err)}), 400


@users.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = mongo.db.users.find_one({"username": username})
    
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful", "user_id": str(user["_id"])}), 200
    return jsonify({"message": "Invalid credentials"}), 401
