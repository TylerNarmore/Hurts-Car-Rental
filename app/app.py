from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from app.data_objects import vehicles
from app.sanitize import *


app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return ''' 
    <html>    
        <body>
            <img src="static/img/logo.jpg" alt="Slight Typo in the logo" style="max-width:100%;max-height=100%">
        </body>
    </html>
    '''


#Admin Calls
@app.route('/inventory', methods=["POST"])
def add_vehicles():
    vehicle_information = request.get_json()
    err = vehicles.add_vehicles(vehicle_information)
    if (err == 0):
        return("400: vehicleID already in use")
    else:
        return("201")


@app.route('/inventory', methods=["PATCH"])
def reset_vehicle_status():
    vehicles.reset_vehicles_status()
    return(jsonify(status="200"))


@app.route('/inventory/<vehicleID>', methods=["DELETE"])
def delete_vehicle(vehicleID):
    vehicles.delete_vehicle(vehicleID)
    return(jsonify(status="200"))


@app.route('/reservations', methods=["GET"])
def search_reservations():
    search_terms = request.args
    search_terms = sanitize_search(search_terms)
    print(len(search_terms))
    search_results = vehicles.search_reservations(search_terms)
    if(search_results[0] == '200'):
        return jsonify(status=search_results[0], vehicles=search_results[1])
    else:
        return jsonify(status=search_results[0], message=search_results[1])



#User Functions
@app.route('/inventory', methods=["GET"])
def search_vehicle():
    #use request.args.get()
    search_terms = request.args
    search_terms = sanitize_search(search_terms)
    search_results = vehicles.find_vehicle(search_terms)
    if(search_results[0] == '200'):
        return jsonify(status=search_results[0], vehicles=search_results[1])
    else:
        return jsonify(status=search_results[0], message=search_results[1])


@app.route('/purchase/<vehicleID>', methods=['POST'])
def purchase_vehicle(vehicleID):
    reservation_information = request.get_json()
    vehicles.purchase_vehicle(reservation_information)
    return("200")


def main():
    app.run(host="0.0.0.0", debug=True)