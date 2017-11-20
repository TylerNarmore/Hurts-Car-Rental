from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from app.data_objects import vehicles


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
def add_vehicle():
    vehicle_information = request.get_json()
    err = vehicles.add_vehicle(vehicle_information)
    if (err == 0):
        return("400: vehicleID already in use")
    else:
        return("201")


@app.route('/inventory', methods=["PATCH"])
def reset_vehicle_status():
    vehicles.reset_vehicles_status()


@app.route('/inventory/<vehicleID>', methods=["DELETE"])
def delete_vehicle(vehicleID):
    vehicles.delete_vehicle(vehicleID)
    return("200")


#User Functions
@app.route('/inventory', methods=["GET"])
def search_vehicle():
    #use request.args.get()
    search_terms = request.args
    found_vehicles = vehicles.find_vehicle(search_terms)

    return jsonify(found_vehicles)


@app.route('/purchase/<vehicleID>', methods=['POST'])
def purchase_vehicle(vehicleID):
    reservation_information = request.get_json()
    vehicles.purchase_vehicle(reservation_information)


def main():
    app.run(host="0.0.0.0", debug=True)