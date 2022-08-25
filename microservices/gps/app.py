import requests
from flask import Flask, request, jsonify, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps

# creates Flask object
app = Flask(__name__)

api_key = "AIzaSyD-HPqZ6715o4r5STSx5mGtlx8vqjTLZNc"


@app.route('/gps', methods =['POST'])
def trip_request():
    data = request.json 
   
    address = data.get('address').replace(" ", "+") + "+VN"

    url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, api_key)
    response = requests.get(url, ploads)

    return response.json()

@app.route('/gps-example-1', methods =['POST'])
def gps_example_1():
    return jsonify({
        'lat' : '10.7970171',
        'long': '106.7031929'
    }), 201    

@app.route('/gps-example-2', methods =['POST'])
def gps_example_2():
    return jsonify({
        'lat' : '10.87038795',
        'long': '106.77833429198822'
    }), 201    

if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    # import logging
    # logging.basicConfig(filename='logging.log',level=logging.DEBUG)

    app.run(debug=True, host='0.0.0.0', port=5004)