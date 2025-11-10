from flask import Blueprint, jsonify


home_bp= Blueprint('home', __name__, url_prefix='/')

@home_bp.route('/')
def home():
    """
    Endpoint racine
    ---
    responses:
      200:
        description: Message d'accueil
    """
    return jsonify({
        "message": "Bienvenue sur l'API NHL Canadiens v1",
        "routes": ["/games", "/users", "/votes"]
    })