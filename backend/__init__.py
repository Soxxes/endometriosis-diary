from flask import Flask
from backend.extensions import mongo
from backend.routes import main


def create_flask_app():
    app = Flask(__name__)

    # load configurations
    app.config.from_object("backend.config.Config")

    # init extensions
    mongo.init_app(app)

    # register Blueprints
    app.register_blueprint(main, url_prefix="/api/users")

    return app
