from app.database import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    number = db.Column(db.Integer)
    position = db.Column(db.String(5))
    shoots_catches = db.Column(db.String(1))
    height_cm = db.Column(db.Integer)
    weight_kg = db.Column(db.Integer)
    birth_date = db.Column(db.Date)
    birth_city = db.Column(db.String(50))
    birth_state = db.Column(db.String(50))