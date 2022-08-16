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
app.app_context().push()

# driver & customer list 
drivers = []
customers = []
index = -1


# register trip
@app.route('/driver-register-trip', methods =['POST'])
def create():
    data = request.json 
  
    if None:
        drivers.append(data.get('username'))

        return make_response('Successfully register.', 201)
    else:
        return make_response('Error.', 202)

@app.route('/passenger-register-trip', methods =['POST'])
def create():
    data = request.json 

    if None:
        passengers.append(data.get('username'))

        return make_response('Successfully register.', 201)
    else:
        return make_response('Error.', 202)
# ok




# Trip Database Route
# create route
@app.route('/create-trip', methods =['POST'])
def create():
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
  
        return make_response('Successfully created.', 201)
    else:
        # returns 202 if trip already exists
        return make_response('Trip already exists.', 202)



if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug = True)