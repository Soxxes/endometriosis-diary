from flask import Blueprint, request, jsonify
from backend.extensions import mongo


foods = Blueprint('foods', __name__)

@foods.route('/search', methods=['GET'])
def search_food():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    # use a case-insensitive search with regex
    results = mongo.db.foodCollection.find({"name": {"$regex": query, "$options": "i"}}).limit(5)

    food_items = []
    for product in results:
        food_items.append({
            "product_name": product.get("product_name"),
            "brand": product.get("brands", "Unknown"),
            "serving_size": product.get("serving_size", "100g"),
            "nutrients": {
                "calories": product.get('nutriments', {}).get('energy-kcal_100g'),
                "protein": product.get('nutriments', {}).get('proteins_100g'),
                "carbs": product.get('nutriments', {}).get('carbohydrates_100g'),
                "fat": product.get('nutriments', {}).get('fat_100g'),
                "fiber": product.get('nutriments', {}).get('fiber_100g'),
                "sugar": product.get('nutriments', {}).get('sugars_100g'),
                "magnesium": product.get('nutriments', {}).get('magnesium_100g'),
                "potassium": product.get('nutriments', {}).get('potassium_100g')
            }
        })
    
    return jsonify({"success": True, "results": food_items}), 200

