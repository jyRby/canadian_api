from flask import Blueprint, jsonify
from ..models import Game
from datetime import date

games_bp = Blueprint('games', __name__, url_prefix='/games')

def format_game(game):
    return {
        "id": game.id,
        "season": game.season,
        "game_type": game.game_type,
        "date": game.game_date.isoformat() if isinstance(game.game_date, date) else game.game_date,
        "home_team": game.home_team,
        "home_score": game.home_score,
        "away_team": game.away_team,
        "away_score": game.away_score
    }

@games_bp.get('/')
def get_all_games():
    """
    Retourne tous les matchs
    ---
    tags:
      - Games
    responses:
      200:
        description: Liste complète des matchs
        content:
          application/json:
            example:
              - id: 2025010015
                season: 20252026
                game_type: 1
                date: "2025-09-22"
                home_team: "Canadiens"
                home_score: 2
                away_team: "Penguins"
                away_score: 1
      404:
        description: Aucun match trouvé
        content:
          application/json:
            example:
              error: "Aucun match trouvé"
    """
    games = Game.query.all()
    if not games:
        return jsonify({"error": "Aucun match trouvé"}), 404
    return jsonify([format_game(g) for g in games]), 200

@games_bp.get('/next10')
def get_next_10_games():
    """
    Retourne les 10 prochains matchs
    ---
    tags:
      - Games
    responses:
      200:
        description: Liste des 10 prochains matchs
        content:
          application/json:
            example:
              - id: 2025010026
                season: 20252026
                game_type: 1
                date: "2025-09-23"
                home_team: "Canadiens"
                home_score: 4
                away_team: "Flyers"
                away_score: 2
      404:
        description: Aucun match futur trouvé
        content:
          application/json:
            example:
              error: "Aucun match trouvé"
    """
    games = Game.query.filter(Game.game_date >= date.today).order_by(Game.game_date.asc()).limit(10).all()
    if not games:
        return jsonify({"error": "Aucun match trouvé"}), 404
    return jsonify([format_game(g) for g in games]), 200

@games_bp.get('/last10')
def last10():
    """
    Retourne les 10 derniers matchs
    ---
    tags:
      - Games
    responses:
      200:
        description: Liste des 10 derniers matchs
        content:
          application/json:
            example:
              - id: 2025010015
                season: 20252026
                game_type: 1
                date: "2025-09-22"
                home_team: "Canadiens"
                home_score: 2
                away_team: "Penguins"
                away_score: 1
      404:
        description: Aucun match passé trouvé
        content:
          application/json:
            example:
              error: "Aucun match trouvé"
    """
    games = Game.query.filter(Game.game_date < date.today).order_by(Game.game_date.desc()).limit(10).all()
    if not games:
        return jsonify({"error": "Aucun match trouvé"}), 404
    return jsonify([format_game(g) for g in games]), 200