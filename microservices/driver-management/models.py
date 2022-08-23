
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Database ORMs
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True)
    email = db.Column(db.String(70))
    phone = db.Column(db.String(70))
    seed = db.Column(db.String(70))  # 4 or 7
    licence_plate = db.Column(db.String(70))
    money = db.Column(db.Float)
