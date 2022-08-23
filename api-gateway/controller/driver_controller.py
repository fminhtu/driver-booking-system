from urllib import request
from flask import Blueprint, request, jsonify, make_response
import requests
import jwt
from models import db, User
import config

from functools import wraps

driver_controller = Blueprint('driver_controller', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(
                token, config.configBooking['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query\
                .filter_by(public_id=data['public_id'])\
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated


@driver_controller.route('/trip/save-trip', methods=['POST'])
# @token_required
def accept_passenger_by_driver(current_user):
    data = request.json
    role = data.get('role')
    response = ""

    if role == 'driver':
        response = requests.post(
            'http://127.0.0.1:5004/save-trip', json=request.json)
    else:
        return jsonify({'message': 'error'}), 401

    return response.json()
