# flask imports
from flask import Flask, request, jsonify, make_response

import uuid # for public id
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import db, Trip

# creates Flask object
app = Flask(__name__)
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'your secret key'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/trip.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object

# initialize dabasae
db.init_app(app)
db.create_all(app=app)
app.app_context().push()

# driver & customer list 
drivers = []
customers = []
index = -1


# register trip
@app.route('/driver-register-trip', methods =['POST'])
def createDriver():
    data = request.json 
  
    if None:
        drivers.append(data.get('username'))

        return jsonify({'message' : 'Successfully registered.'}), 201
    else:
        return jsonify({'message' : 'Error.'}), 401

@app.route('/passenger-register-trip', methods =['POST'])
def createPassenger():
    data = request.json 

    if None:
        passengers.append(data.get('username'))

        return jsonify({'message' : 'Successfully registered.'}), 201
    else:
        return jsonify({'message' : 'Error.'}), 401
        
# check ready



# save route
@app.route('/save-trip', methods =['POST'])
def createTrip():
    # creates a dictionary of the form data
    data = request.json 
  
    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')
  
    # checking for existing trip
    trip = Trip.query\
        .filter_by(email = email)\
        .first()
    if not trip:
        # database ORM object
        trip = Trip(
            public_id = str(uuid.uuid4()),
            name = name,
            email = email,
            password = generate_password_hash(password)
        )
        # insert trip
        db.session.add(trip)
        db.session.commit()
  
        return jsonify({'message' : 'Successfully created.'}), 201
    else:
        # returns 401 if trip already exists
        return jsonify({'message' : 'Trip already exists.'}), 401


if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug = True)