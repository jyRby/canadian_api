from app.database import db

class Game(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    season = db.Column(db.Integer)
    game_type = db.Column(db.Integer)
    game_date = db.Column(db.Date)
    home_team = db.Column(db.String(50))
    home_score = db.Column(db.Integer)
    away_team = db.Column(db.String(50))
    away_score = db.Column(db.Integer)