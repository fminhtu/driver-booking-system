# flask imports
from flask import Flask, request, jsonify, make_response

import uuid # for public id
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import db, User

import requests
import os


# microservice list



# creates Flask object
app = Flask(__name__)
# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'your secret key'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/account.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object

# initialize dabasae
db.init_app(app)
app.app_context().push()
# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated
  
# User Database Route
# this route sends back list of users
@app.route('/user', methods =['GET'])
@token_required
def get_all_users(current_user):
    # querying the database
    # for all the entries in it
    users = User.query.all()
    # converting the query objects
    # to list of jsons
    output = []
    for user in users:
        # appending the user data json
        # to the response list
        output.append({
            'public_id': user.public_id,
            'username' : user.username
        })
  
    return jsonify({'users': output})
  
# route for logging user in
@app.route('/login', methods =['POST'])
def login():
    # creates dictionary of form data
    auth = request.json
  
    if not auth or not auth.get('username') or not auth.get('password'):
        # returns 401 if any username or / and password is missing
        return jsonify({'message' : 'Could not verify'}), 401
  
    user = User.query\
        .filter_by(username=auth.get('username'))\
        .first()
  
    if not user:
        # returns 401 if user does not existz
        return jsonify({'message' : 'Could not verify'}), 401
  
    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")
  
        return make_response(jsonify({'token' : token}), 201)
    # returns 403 if password is wrong
    return jsonify({'message' : 'Could not verify'}), 401
    

# send request create new profile to microservices

def create_driver(request):
    response = requests.post('http://127.0.0.1:5001/create', json=request.json)

    # sucessfully created a driver
    if response.status_code == 201: 
        return jsonify({'message' : 'Successfully created'}), 201

    return jsonify({'message' : 'Cannot created'}), 401

def create_passenger(request):
    response = requests.post('http://127.0.0.1:5002/create', json=request.json)

    # sucessfully created a driver
    if response.status_code == 201: 
        return jsonify({'message' : 'Successfully created'}), 201
 
    return jsonify({'message' : 'Cannot created'}), 401

# signup route
@app.route('/register', methods =['POST'])
def register():
    # creates a dictionary of the form data
    data = request.json 
  
    # gets name, email and password
    username = data.get('username')
    password = data.get('password')
  
    # checking for existing user
    user = User.query\
        .filter_by(username=username)\
        .first()
    if not user:
        # database ORM object
        user = User(
            public_id = str(uuid.uuid4()),
            username = username,
            password = generate_password_hash(password)
        )
        # insert user
        db.session.add(user)
        db.session.commit()

        role = data.get('role')

        if role == 'driver':
            #create driver profile
            create_driver(request)
        elif role == 'passenger':
            #create passenger profile
            create_passenger(request)

        return jsonify({'message' : 'Successfully registered'}), 201
    else:
        # returns 401 if user already exists
        return jsonify({'message' : 'User already exists. Please Log in.'}), 401

# edit a profile
@app.route('/edit-profile', methods =['POST'])
@token_required
def edit_passenger_profile(current_user):
    data = request.json 
    role = data.get('role')
    response = ""

    if role == 'driver':
        response = requests.post('http://127.0.0.1:5001/edit', json=request.json)
    elif role == 'passenger':
        response = requests.post('http://127.0.0.1:5002/edit', json=request.json)
    else:
        return jsonify({'message' : 'error'}), 401  

    return response.json()
    
# get a profile
@app.route('/get-profile', methods =['POST'])
@token_required
def get_driver_profile(current_user):
    data = request.json 
    role = data.get('role')
    if role == 'driver':
        response = requests.get('http://127.0.0.1:5001/get', json=request.json)

    elif role == 'passenger':
        response = requests.get('http://127.0.0.1:5002/get', json=request.json)
    else:   
        return jsonify({'message' : 'error'}), 401  

    return response.json()
   

# port = int(os.environ.get('PORT', 5000))
if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug=True, host='0.0.0.0', port=5000)