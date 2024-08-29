from flask import Blueprint
from .users import users


main = Blueprint('main', __name__)

main.register_blueprint(users)
