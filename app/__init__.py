import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from dotenv import load_dotenv

from app.database import db, initialize_db
from app.models import *

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Configs
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    Swagger(app)

    # Blueprints
    from .routes.users import users_bp
    from .routes.games import games_bp
    from .routes.votes import votes_bp
    from .routes.home import home_bp
    from .routes.players import players_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(votes_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(players_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return {"error": "Endpoint introuvable"}, 404

    @app.errorhandler(500)
    def internal_error(e):
        return {"error": "Erreur interne du serveur"}, 500

    with app.app_context():
        db.create_all()
        initialize_db(app)

    return app