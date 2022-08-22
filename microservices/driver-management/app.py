# flask imports
from flask import Flask, request, jsonify, make_response

import uuid # for public id
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import db, Driver

# creates Flask object
app = Flask(__name__)
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'your secret key'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/driver.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object

# initialize dabasae
db.init_app(app)
db.create_all(app=app)
app.app_context().push()
  
# Driver Database Route
# this route sends back list of drivers
@app.route('/get', methods=['GET'])
def get_all_drivers():
    # querying the database
    # for all the entries in it
    data = request.json 
    username = data.get('username')

    drivers = driver = Driver.query\
        .filter_by(username=username)\
        .first()

    # converting the query objects
    # to list of jsons
    output = []
    output.append({
        'username': driver.username,
        'email': driver.email,
        'phone': driver.phone,
        'seed': driver.seed,
        'licence_plate': driver.licence_plate
    })
  
    return jsonify({'drivers': output})
  
# route for logging driver in
@app.route('/edit', methods=['POST'])
def login():
    # creates dictionary of form data
    # creates a dictionary of the form data
    data = request.json 
  
    # get data from json data
    username, email, phone = data.get('username'), data.get('email'), data.get('phone')
    seed, licence_plate = data.get('seed'), data.get('licence_plate')

    # checking for existing driver
    driver = Driver.query\
        .filter_by(username = username)\
        .first()

    if driver:
        driver.username = username
        driver.email = email
        driver.phone = phone
        driver.seed = seed
        driver.licence_plate = licence_plate
        db.session.commit()
  
        return jsonify({'message' : 'Successfully edited.'}), 201 
    else:
        # returns 401 if driver already exists
        return jsonify({'message' : 'Driver is not exists'}), 401 
    
  
# create route
@app.route('/create', methods=['POST'])
def create():
    # creates a dictionary of the form data
    data = request.json 
  
    # get data from json data
    username, email, phone = data.get('username'), data.get('email'), data.get('phone')
    seed, licence_plate = data.get('seed'), data.get('licence_plate')
    # checking for existing driver
    driver = Driver.query\
        .filter_by(username=username)\
        .first()
    if not driver:
        # database ORM object
        driver = Driver(
            username = username,
            email = email,
            phone = phone,
            seed = seed,
            licence_plate = licence_plate
        )
        # insert driver
        db.session.add(driver)
        db.session.commit()
  
        return jsonify({'message' : 'Successfully created.'}), 201 
    else:
        # returns 401 if driver already exists
        return jsonify({'message' : 'Driver already exists.'}), 401 



if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug=True, host='0.0.0.0', port=5001)