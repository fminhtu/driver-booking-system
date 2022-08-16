
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Database ORMs
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)

    passenger = db.Column(db.String(80))
    driver = db.Column(db.String(80))

    origin_lat = db.Column(db.String(80))
    origin_long = db.Column(db.String(80))

    dest_lat = db.Column(db.String(80))
    dest_long = db.Column(db.String(80))

    time = db.Column(db.String(80))



