# flask imports
from flask import Flask, request, jsonify, make_response

import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import db, Passenger

# creates Flask object
app = Flask(__name__)
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'your secret key'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nintendo123@172.104.167.232:8201/call-center'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object

# initialize dabasae
db.init_app(app)
db.create_all(app=app)
app.app_context().push()

# Passenger Database Route
# this route sends back list of passengers


@app.route('/get', methods=['GET'])
def get_all_passengers():
    # querying the database
    # for all the entries in it
    data = request.json
    username = data.get('username')

    passengers = passenger = Passenger.query\
        .filter_by(username=username)\
        .first()


    if (passenger is None):
        return jsonify({'passengers': "not found"}), 400
    # converting the query objects
    # to list of jsons
    output = []
    output.append({
        'username': passenger.username,
        'email': passenger.email,
        'phone': passenger.phone
    })

    return jsonify({'passengers': output}), 200

# route for logging passenger in


@app.route('/edit', methods=['POST'])
def login():
    # creates dictionary of form data
    # creates a dictionary of the form data
    data = request.json

    # get data from json data
    username, email, phone = data.get(
        'username'), data.get('email'), data.get('phone')

    # checking for existing passenger
    passenger = Passenger.query\
        .filter_by(username=username)\
        .first()

    if passenger:
        passenger.username = username
        passenger.email = email
        passenger.phone = phone
        db.session.commit()

        return jsonify({'message': 'Successfully edited.'}), 201
    else:
        # returns 401 if passenger already exists
        return jsonify({'message': 'Passenger is not exists'}), 401


# create route
@app.route('/create', methods=['POST'])
def create():
    # creates a dictionary of the form data
    data = request.json

    # get data from json data
    username, email, phone = data.get(
        'username'), data.get('email'), data.get('phone')

    # checking for existing passenger
    passenger = Passenger.query\
        .filter_by(username=username)\
        .first()
    if not passenger:
        # database ORM object
        passenger = Passenger(
            username=username,
            email=email,
            phone=phone
        )
        # insert passenger
        db.session.add(passenger)
        db.session.commit()

        return jsonify({'message': 'Successfully created.'}), 201
    else:
        # returns 401 if passenger already exists
        return jsonify({'message': 'Passenger already exists.'}), 401


if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug=True, host='0.0.0.0', port=5002)
