from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
from app.data_objects import vehicles
#from redis import Redis

app = Flask(__name__)
CORS(app)
#redis = Redis(host='redis', port=6379)

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
    #test = Vehicle(vehicle_information)
    return("201")

@app.route('/inventory', methods=["PATCH"])
def reset_vehicle_status():
    vehicles.reset_vehicles_status()

@app.route('/inventory/<vehicleID>', methods=["DELETE"])
def delete_vehicle(vehicleID):
    vehicles.delete_vehicle(vehicleID)

#User Functions
@app.route('/inventory', methods=["GET"])
def search_vehicle():
    #use request.args.get()
    search_terms = request.args
    vehicles.find_vehicle(search_terms)

@app.route('/purchase/<vehicleID>/<startDate>&<endDate>', methods=['POST'])
def purchase_vehicle(vehicleID,startDate, endDate):
    vehicles.purchase_vehicle(vehicleID, startDate, endDate)


def main():
    app.run(host="0.0.0.0", debug=True)