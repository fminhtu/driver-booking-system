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
queue = {} # {driver: passenger}
location = {}  # {driver: current location}
index = -1


def create_trip(request):
    # creates a dictionary of the form data
    data = request.json

    # get data from json data
    passenger = data.get('passenger')
    driver = data.get('driver')

    origin_address = data.get('origin_address')
    origin_lat = data.get('origin_lat')
    origin_long = data.get('origin_long')

    dest_address = data.get('dest_address')
    dest_lat = data.get('dest_lat')
    dest_long = data.get('dest_long')

    time = data.get('time')
    payment = data.get('payment')
    status = data.get('status')

    trip = Trip(
        passenger_username=passenger,
        driver_username=driver,
        origin_address=origin_address,
        origin_lat=origin_lat,
        origin_long=origin_long,
        dest_address=dest_address,
        dest_lat=dest_lat,
        dest_long=dest_long,
        time=time,
        payment=payment,
        status=status
    )
    # insert trip
    db.session.add(trip)
    db.session.commit()

    return jsonify({'message': 'Successfully created.'}), 201

@app.route('/trip-request', methods =['POST'])
def trip_request():
    data = request.json 
    role = data.get('role')
    username = data.get('username')

    if role == 'driver':
        if username in queue.keys():
            return jsonify({
                'message' : "OK",
                'passenger': queue[username],
                'driver': username
            }), 201

        queue[username] = None
        return jsonify({'message' : 'Wait'}), 201

    elif role == 'passenger':
        if username in queue.values():    
            for key in queue.keys():
                if queue[key] == username:
                    return jsonify({
                        'message' : "OK",
                        'passenger': username,
                        'driver': key
                    }), 201

            
        else:
            for key in queue.keys():
                if queue[key] == None:
                    queue[key] = username
                    create_trip(request)            # create new trip
                    location[key] = [None, None]            # init current location of driver
                    return jsonify({
                        'message' : "Wait",
                        'passenger': username,
                        'driver': key
                    }), 201

    return jsonify({'message' : 'Try again'}), 400


@app.route('/update-gps', methods =['POST'])
def update_gps():
    data = request.json 
    username = data.get('username')
    latitude = data.get('lat')
    longitude  = data.get('long')
    
    if username not in location.keys():   
        return jsonify({'message' : 'driver is not found'}), 401

    location[username] = [latitude, longitude]
    return jsonify({'message' : 'Updated'}), 201

@app.route('/current-gps', methods =['POST'])
def get_current_gps():
    data = request.json 
    username = data.get('username')
    
    if username not in location.keys():   
        return jsonify({'message' : 'driver is not found'}), 401

    return jsonify({
        'message' : 'current gps', 
        'lat': location[username][0],
        'long': location[username][1]
    }), 201


@app.route('/end-trip', methods =['POST'])
def end_trip():
    data = request.json 
    username = data.get('username')
    
    if username not in location.keys():   
        return jsonify({'message' : 'driver is not found'}), 401

    queue.pop(username, None)

    return jsonify({
        'message' : 'end trip'
    }), 201


if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug = True, port=5003)