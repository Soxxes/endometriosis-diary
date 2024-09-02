from flask import Blueprint
from .users import users
from .foods import foods
from .food_entries import food_entries


users_bp = Blueprint('users', __name__)
users_bp.register_blueprint(users)

foods_bp = Blueprint('foods', __name__)
foods_bp.register_blueprint(foods)

food_entries_bp = Blueprint('food_entries', __name__)
food_entries_bp.register_blueprint(food_entries)
