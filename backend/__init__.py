from flask import Flask
from backend.extensions import mongo
from backend.routes import users_bp, foods_bp, food_entries_bp


def create_flask_app():
    app = Flask(__name__)

    # load configurations
    app.config.from_object("backend.config.Config")

    # init extensions
    mongo.init_app(app)

    # register Blueprints
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(foods_bp, url_prefix="/api/foods")
    app.register_blueprint(food_entries_bp, url_prefix="/api/foodEntries")

    return app
