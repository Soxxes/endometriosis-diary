from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from backend.extensions import mongo
from backend.models.user import User


users = Blueprint('users', __name__)

@users.route('/add', methods=['POST'])
def add_user():
    user_data = request.json

    validated_data, errors = User.validate(user_data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    user = User(**validated_data)
    user_id = user.save()
    
    return jsonify({"message": "User added", "id": str(user_id)}), 201
