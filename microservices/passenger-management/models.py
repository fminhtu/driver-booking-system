
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Database ORMs
class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text(70), unique = True)
    email = db.Column(db.Text(70))
    phone = db.Column(db.Text(70))
