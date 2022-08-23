
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Database ORMs
class Trip(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    passenger_username = db.Column(db.String(80))
    driver_username = db.Column(db.String(80))

    origin_address = db.Column(db.String(80))
    origin_lat = db.Column(db.String(80))
    origin_long = db.Column(db.String(80))

    dest_address = db.Column(db.String(80))
    dest_lat = db.Column(db.String(80))
    dest_long = db.Column(db.String(80))

    time = db.Column(db.DateTime)

    status = db.Column(db.String(80))

    price = db.Column(db.Float)



