from flask import Blueprint, jsonify, request
from app.models import Player

players_bp = Blueprint('players', __name__, url_prefix='/players')

def format_player(player):
    return {
        "id": player.id,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "number": player.number,
        "position": player.position,
        "shoots_catches": player.shoots_catches,
        "height_cm": player.height_cm,
        "weight_kg": player.weight_kg,
        "birth_date": player.birth_date.isoformat() if player.birth_date else None,
        "birth_city": player.birth_city,
        "birth_state": player.birth_state
    }

@players_bp.get('/')
def get_all_players():
    """
    Retourne tous les joueurs ou filtre par position
    ---
    parameters:
      - name: position
        in: query
        type: string
        description: Filtrer par position (F, D, G)
    responses:
      200:
        description: Liste de joueurs
        content:
          application/json:
            example: [
              {
                "id": 8476981,
                "first_name": "Josh",
                "last_name": "Anderson",
                "number": 17,
                "position": "R",
                "shoots_catches": "R",
                "height_cm": 191,
                "weight_kg": 103,
                "birth_date": "1994-05-07",
                "birth_city": "Burlington",
                "birth_state": "ON"
              }
            ]
      404:
        description: Aucun joueur trouvé
        content:
          application/json:
            example: {"error": "Aucun joueur trouvé"}
    """
    query = Player.query
    position = request.args.get('position')
    if position:
        query = query.filter(Player.position == position.upper())

    players = query.all()
    if not players:
        return jsonify({"error": "Aucun joueur trouvé"}), 404

    return jsonify([format_player(p) for p in players])


@players_bp.get('/<int:player_id>')
def get_player(player_id):
    """
    Retourne un joueur par son ID
    ---
    parameters:
      - name: player_id
        in: path
        type: integer
        required: true
        description: ID du joueur
    responses:
      200:
        description: Détails du joueur
        content:
          application/json:
            example:
              {
                "id": 8476981,
                "first_name": "Josh",
                "last_name": "Anderson",
                "number": 17,
                "position": "R",
                "shoots_catches": "R",
                "height_cm": 191,
                "weight_kg": 103,
                "birth_date": "1994-05-07",
                "birth_city": "Burlington",
                "birth_state": "ON"
              }
      404:
        description: Joueur non trouvé
        content:
          application/json:
            example: {"error": "Joueur non trouvé"}
    """
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Joueur non trouvé"}), 404
    return jsonify(format_player(player))