# flask imports
from flask import Flask, request, jsonify, make_response

import uuid # for public id
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import db, Trip
from datetime import date
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
information = {}    # {driver: trip information}
index = -1



def save_trip(data):
    # get data from json data
    passenger = data.get('passenger')
    driver = data.get('driver')

    origin_address = data.get('origin_address')
    origin_lat = data.get('origin_lat')
    origin_long = data.get('origin_long')

    dest_address = data.get('dest_address')
    dest_lat = data.get('dest_lat')
    dest_long = data.get('dest_long')

    now = datetime.now()
    time = now.strftime("%d/%m/%Y %H:%M:%S")
    payment = "65000"
    status = "finished"

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

@app.route('/add-trip', methods =['POST'])
def add_trip():
    save_trip(request.json)
    return jsonify({'message': 'Successfully added.'}), 201

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
                    location[key] = [None, None]            # init current location of driver
                    information[key] = data

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

@app.route('/trip-information', methods =['POST'])
def get_current_gps():
    data = request.json 
    username = data.get('username')
    
    if username not in queue.keys():   
        return jsonify({'message' : 'driver is not found'}), 401

    if username not in location.keys():   
        return jsonify({'message' : 'driver is not found'}), 401
    
    if username not in information.keys():   
        return jsonify({'message' : 'driver is not found'}), 401

    return jsonify({
        'message' : 'current gps', 
        'lat': location[username][0],
        'long': location[username][1],
        'information': information[username]
    }), 201


@app.route('/end-trip', methods =['POST'])
def end_trip():
    data = request.json 
    username = data.get('username')
    
    if username not in queue.keys():   
        return jsonify({'message' : 'driver is not found'}), 401

    if username not in location.keys():   
        return jsonify({'message' : 'driver is not found'}), 401

    if username in information.keys():
        save_trip(information[username])
        # print("saved")
        del information[username]        

    queue.pop(username, None)
    location.pop(username, None)

    return jsonify({
        'message' : 'end trip'
    }), 201

@app.route('/leave-trip', methods =['POST'])
def leave_trip():
    data = request.json 
    username = data.get('username')

    if username not in queue.keys():   
        return jsonify({'message' : 'driver is not found'}), 401
    else:
        del queue[username]

    return jsonify({
        'message' : 'driver leaved'
    }), 201

@app.route('/get-all-trip', methods =['GET'])
def get_all_trip():
    # querying the database
    # for all the entries in it
    trips = Trip.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for trip in trips:
        # appending the user data json
        # to the response list
        output.append({
            "passenger_username": trip.passenger_username,
            "driver_username": trip.driver_username,
            "origin_address": trip.origin_address,
            "origin_lat": trip.origin_lat,
            "origin_long": trip.origin_long,
            "dest_address": trip.dest_address,
            "dest_lat": trip.dest_lat,
            "dest_long": trip.dest_long,
            "time": trip.time,
            "payment": trip.payment,
            "status": trip.status
        })
  
    return jsonify({"trips": output}), 201


if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug = True, port=5003)