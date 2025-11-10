import os
import requests
from datetime import datetime, timedelta
from .database import db
from app.models import Game, Player

API_URL_GAMES = "https://api-web.nhle.com/v1/club-schedule-season/MTL/20252026"
API_URL_PLAYERS = "https://api-web.nhle.com/v1/roster/MTL/current"


def db_is_games_empty():
    try:
        return Game.query.count() == 0
    except Exception as e:
        print(f"Erreur DB: {e}")
        return True


def fetch_games_from_nhl():
    try:
        response = requests.get(API_URL_GAMES, timeout=10)
        response.raise_for_status()
        return response.json().get("games", [])
    except requests.RequestException as e:
        print(f"Erreur API NHL: {e}")
        return []


def populate_games(games_json):
    for g in games_json:
        try:
            game_date = datetime.strptime(g["gameDate"], "%Y-%m-%d").date()
            home = g["homeTeam"]["commonName"]["default"]
            away = g["awayTeam"]["commonName"]["default"]
            home_score = g["homeTeam"].get("score")
            away_score = g["awayTeam"].get("score")

            game = Game(
                id=g["id"],
                season=g["season"],
                game_type=g["gameType"],
                game_date=game_date,
                home_team=home,
                home_score=home_score,
                away_team=away,
                away_score=away_score
            )
            db.session.merge(game)
        except Exception as e:
            print(f"Erreur insertion match {g.get('id')}: {e}")
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erreur commit DB: {e}")


def update_yesterday_games():
    yesterday = datetime.now().date() - timedelta(days=1)
    games = Game.query.filter(Game.game_date == yesterday).all()
    if not games:
        print("Aucun match hier")
        return
    nhl_games = fetch_games_from_nhl()
    for g in games:
        match_data = next((x for x in nhl_games if x["id"] == g.id), None)
        if match_data:
            try:
                g.home_score = match_data["homeTeam"].get("score")
                g.away_score = match_data["awayTeam"].get("score")
                g.game_state = match_data.get("gameState")
            except Exception as e:
                print(f"Erreur update match {g.id}: {e}")
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erreur commit update DB: {e}")


def db_is_players_empty():
    try:
        return Player.query.count() == 0
    except Exception as e:
        print(f"Erreur DB players: {e}")
        return True


def fetch_players_from_nhl():
    try:
        resp = requests.get(API_URL_PLAYERS, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        print(f"Erreur API NHL roster: {e}")
        return {}


def populate_players():
    data = fetch_players_from_nhl()
    if not data:
        return

    for category in ["forwards", "defensemen", "goalies"]:
        for p in data.get(category, []):
            try:
                player = Player(
                    id=p["id"],
                    first_name=p["firstName"]["default"],
                    last_name=p["lastName"]["default"],
                    number=p.get("sweaterNumber"),
                    position=p.get("positionCode"),
                    shoots_catches=p.get("shootsCatches"),
                    height_cm=p.get("heightInCentimeters"),
                    weight_kg=p.get("weightInKilograms"),
                    birth_date=datetime.strptime(p.get("birthDate"), "%Y-%m-%d").date()
                    if p.get("birthDate") else None
                )
                db.session.merge(player)
            except Exception as e:
                print(f"Erreur insertion player {p.get('id')}: {e}")
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erreur commit DB players: {e}")


def initialize_db(app=None):
    if app:
        with app.app_context():
            _initialize_db_core()
    else:
        _initialize_db_core()


def _initialize_db_core():
    if db_is_games_empty() or db_is_players_empty():
        print("DB vide → peuplement initial games + players")
        games_json = fetch_games_from_nhl()
        populate_games(games_json)
        populate_players()
    else:
        print("DB existante → mise à jour hier + update players")
        update_yesterday_games()
        populate_players()