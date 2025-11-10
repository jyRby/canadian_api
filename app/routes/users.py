from flask import Blueprint, jsonify, request
from app.models.User import User
from app import db
from app import bcrypt
from flask_jwt_extended import create_access_token

users_bp = Blueprint('users', __name__, url_prefix='/users')

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(hashed, password):
    return bcrypt.check_password_hash(hashed, password)

@users_bp.post('/register')
def register_user():
    """
    Crée un utilisateur
    ---
    parameters:
      - in: body
        name: body
        schema:
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Utilisateur créé
      400:
        description: Nom d'utilisateur ou mot de passe manquant
      409:
        description: Nom d'utilisateur déjà pris
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Nom d'utilisateur et mot de passe requis"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Nom d'utilisateur déjà pris"}), 409

    user = User(username=username, password=hash_password(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Utilisateur créé!"}), 201

@users_bp.post('/login')
def login_user():
    """
    Connecte un utilisateur et retourne un token JWT
    ---
    parameters:
      - in: body
        name: body
        schema:
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Token JWT
      400:
        description: Requête mal formée
      401:
        description: Identifiants invalides
    """
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Requête mal formée"}), 400

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not verify_password(user.password, password):
        return jsonify({"error": "Identifiants invalides"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"token": token}), 200