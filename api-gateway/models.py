
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Database ORMs
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    username = db.Column(db.String(80), unique = True)
    password = db.Column(db.String)
    status = db.Column(db.String(80))