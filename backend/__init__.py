from flask import Flask
from backend.extensions import mongo


def create_flask_app():
    app = Flask(__name__)

    # load configurations
    app.config.from_object("backend.config.Config")

    # init extensions
    mongo.init_app(app)

    return app
