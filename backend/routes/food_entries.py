from flask import Blueprint, request, jsonify
from datetime import datetime
from backend.extensions import mongo
from backend.models.food_entry import FoodEntry


food_entries = Blueprint('food_entries', __name__)

@food_entries.route('/add', methods=['POST'])
def add_food_entry():
    data = request.json
    # update nutritions with sum of all nutritions
    nutritions = {}
    for d in data["nutritions"]:
        for nut, value in d.items():
            if nut in nutritions:
                nutritions[nut] += value
            else:
                nutritions[nut] = value
    data["nutritions"] = nutritions
    
    try:
        validated_data, errors = FoodEntry.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400
        
        food_entry = FoodEntry(**validated_data)
        food_entry.save()

        return jsonify({"message": "Food Entry added",
                        "user_id": data["user_id"],
                        "date": data["date"]}), 201

    except ValueError as err:
        return jsonify({"errors": str(err)}), 400
    

@food_entries.route('/get', methods=['GET'])
def get_food_entry():
    data = request.json
    user_id = data['user_id']
    date = data['date']

    if not user_id or not date:
        return jsonify({"error": "user_id and date are required"}), 400

    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        food_entry = FoodEntry.get_by_user_and_date(user_id, date_obj)
        
        if not food_entry:
            return jsonify({"message": "Food entry not found"}), 404

        # convert ObjectId to string for JSON serialization
        food_entry['_id'] = str(food_entry['_id'])

        return jsonify(food_entry), 200

    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400


@food_entries.route('/update/<foodEntry_id>', methods=['PUT'])
def update_food_entry(foodEntry_id):
    data = request.json
    try:
        validated_data, errors = FoodEntry.validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        existing_entry = FoodEntry.get_by_id(foodEntry_id)
        if not existing_entry:
            return jsonify({"message": "Food Entry not found"}), 404
        
        FoodEntry.update(foodEntry_id, validated_data)

        return jsonify({"message": "Food Entry updated"}), 200

    except ValueError as err:
        return jsonify({"errors": str(err)}), 400
