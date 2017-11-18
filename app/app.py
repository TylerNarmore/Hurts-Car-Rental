from flask import Flask, jsonify, abort, request
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    return '''
    <html><body>
    <a href="/hello_world"> Hello</a> World
    '''

@app.route('/hello_world')
def hello2():
	return '''
	<html><body>
	Hello World
	'''

#Admin Calls
@app.route('/inventory', methods=["POST"])
def add_vehicle():
    pass

@app.route('/inventory', methods=["PATCH"])
def reset_vehicle_status():
    pass

@app.route('/inventory/<vehicleID>', methods=["DELETE"])
def delete_vehicle(vehicleID):
    pass

#User Functions
@app.route('/inventory', methods=["GET"])
def search_vehicle():
    #use request.args.get()
    pass

@app.route('/purchase/<vehicleID>', methods=['POST'])
def purchase_vehicle(vehicleID):
    pass

def main():
    app.run(host="0.0.0.0", debug=True)