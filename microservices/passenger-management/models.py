
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Database ORMs
class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(70), unique = True)
    email = db.Column(db.String(70))
    phone = db.Column(db.String(70))
