from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Vote, Player, Game, User
from app import db
import traceback

votes_bp = Blueprint('votes', __name__, url_prefix='/votes')

@votes_bp.post('/')
@jwt_required()
def vote_player():
    """
    Vote pour un joueur étoile
    ---
    parameters:
      - in: body
        name: body
        schema:
          required:
            - game_id
            - player_id
          properties:
            game_id:
              type: integer
            player_id:
              type: integer
    responses:
      201:
        description: Vote enregistré
      400:
        description: Données manquantes
      401:
        description: Token JWT manquant ou invalide
      404:
        description: Match ou joueur introuvable
      422:
        description: Erreur lors de l'enregistrement du vote
    """
    try:
        data = request.get_json()
        if not data or "game_id" not in data or "player_id" not in data:
            return jsonify({"error": "Données manquantes"}), 400

        game_id = int(data["game_id"])
        player_id = int(data["player_id"])
        user_id = int(get_jwt_identity())

        game = Game.query.get(game_id)
        player = Player.query.get(player_id)

        print(f"DEBUG vote : user_id={user_id}, game_id={game_id}, player_id={player_id}")
        print(f" - Game found: {game is not None}")
        print(f" - Player found: {player is not None}")

        if not game or not player:
            return jsonify({"error": "Game ou Player introuvable"}), 422

        vote = Vote(game_id=game.id, player_id=player.id, user_id=user_id)
        db.session.add(vote)
        db.session.commit()

        print("✅ Vote enregistré avec succès")
        return jsonify({"message": "Vote enregistré"}), 201

    except Exception as e:
        db.session.rollback()
        print("❌ ERREUR SQL :", str(e))
        traceback.print_exc()
        return jsonify({"error": f"Erreur lors de l'enregistrement du vote : {str(e)}"}), 422


@votes_bp.get('/top')
def get_top_players():
    """
    Retourne les joueurs avec le plus de votes
    ---
    responses:
      200:
        description: Liste des joueurs et nombre de votes
      404:
        description: Aucun vote enregistré
    """
    results = db.session.query(
        Player.first_name,
        Player.last_name,
        db.func.count(Vote.id).label('votes')
    ).join(Vote, Vote.player_id == Player.id)\
     .group_by(Player.id)\
     .order_by(db.desc('votes'))\
     .all()

    if not results:
        return jsonify({"error": "Aucun vote enregistré"}), 404

    return jsonify([
        {"player": f"{r[0]} {r[1]}", "votes": r[2]} for r in results
    ]), 200


@votes_bp.get('/')
@jwt_required()
def get_user_votes():
    """
    Retourne les votes de l'utilisateur connecté
    ---
    responses:
      200:
        description: Liste des votes de l'utilisateur
      401:
        description: Token JWT manquant ou invalide
      404:
        description: Aucun vote trouvé pour cet utilisateur
    """
    user_id = int(get_jwt_identity())
    votes = Vote.query.filter_by(user_id=user_id).all()

    if not votes:
        return jsonify({"error": "Aucun vote trouvé pour cet utilisateur"}), 404

    return jsonify([
        {"game_id": v.game_id, "player_id": v.player_id} for v in votes
    ]), 200