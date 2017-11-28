import sqlite3
import datetime

dbAddress = 'app/data_objects/hurts_db.db'
valid_query_fields = ['location', 'startDate', 'endDate', 'minPrice', 'maxPrice',
                      'minPassenger', 'make', 'model', 'type',
                      'minMPG', 'gps', 'minChildSeats', 'skiRack', 'snowChains',
                      'leftControl', 'autoTransmission', 'year']

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S')
        return(1)
    except ValueError:
        return(-1)


def add_vehicle(vehicle):
    vehicleID = vehicle["vehicleID"]
    make = vehicle["make"]
    model = vehicle["model"]
    year = vehicle["year"]
    location = vehicle["location"]
    cost = vehicle["cost"]
    passengers = vehicle["passengers"]
    autoTransmission = vehicle["autoTransmission"]
    type = vehicle["type"]
    mpg = vehicle["mpg"]
    gps = vehicle["specialEquipment"]["gps"]
    maxChildSeat = vehicle["specialEquipment"]["maxChildSeat"]
    skiRack = vehicle["specialEquipment"]["skiRack"]
    snowChains = vehicle["specialEquipment"]["snowChains"]
    leftControl = vehicle["specialEquipment"]["leftControl"]

    #DB calls
    try:
        conn = sqlite3.connect(dbAddress)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO inventory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (vehicleID, make, model, year, location, cost, passengers,
                       autoTransmission, type, mpg, gps, maxChildSeat, skiRack,
                       snowChains, leftControl))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError :
        return(0)
    return(1)


def reset_vehicles_status():
    #Remove all reservations from system
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()
    cursor.execute("DELETE * FROM reservation;")
    conn.commit()
    conn.close()
    return(1)


def delete_vehicle(vehicleID):
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE vehicleID=?", [vehicleID])
    conn.commit()
    conn.close()
    return(0)


def find_vehicle(search_terms):
    #Search terms is a dictionary of terms being searched with the category
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()

    #Confirm both dates are present or neither dates are present.
    if not("startDate" in search_terms.keys() and "endDate" in search_terms.keys() or
            (not ("startDate" in search_terms.keys()) and not ("endDate" in search_terms.keys()))):
        return(('400', "Only start date or end date provided"))
    if(len(search_terms.keys()) == 0):
        cursor.execute('SELECT * FROM inventory;')
    for key in search_terms:
        if not(key in valid_query_fields):
            return(('400', "Invalid query field: "+key))

        if(key == 'location'):
            cursor.execute('SELECT * FROM inventory WHERE location = ?;', [search_terms[key]])
        elif(key == 'startDate' or key == 'endDate'):
            if(validate(search_terms['startDate'])==1 and validate(search_terms['endDate'])==1):
                if(datetime.datetime.strptime(search_terms['startDate'], '%Y-%m-%dT%H:%M:%S') > datetime.datetime.strptime(search_terms['endDate'], '%Y-%m-%dT%H:%M:%S')):
                    return(('422', "Error: Start date after end date"))
            else:
                return(('422', "Error: Datetime formatted incorrectly"))
            cursor.execute("SELECT * FROM inventory i WHERE NOT EXISTS (SELECT vehicleID FROM reservation r WHERE i.vehicleID = r.vehicleID AND endDate > ? AND startDate < ?);", (search_terms['startDate'],search_terms['endDate']))
        elif(key == 'minPrice'):
            cursor.execute("SELECT  * FROM inventory WHERE cost >= ?;", [search_terms[key]])
        elif(key == 'maxPrice'):
            cursor.execute("SELECT  * FROM inventory WHERE cost <= ?;", [search_terms[key]])
        elif(key == 'minPassenger'):
            cursor.execute("SELECT * FROM inventory WHERE passengers >= ?;", [search_terms[key]])
        elif(key == 'make'):
            cursor.execute("SELECT * FROM inventory WHERE make = ?;", [search_terms[key]])
        elif(key == 'model'):
            cursor.execute("SELECT * FROM inventory WHERE model = ?;", [search_terms[key]])
        elif(key == 'type'):
            cursor.execute("SELECT * FROM inventory WHERE type = ?", [search_terms[key]])
        elif(key == 'minMPG'):
            cursor.execute("SELECT * FROM inventory WHERE mpg >= ?", [search_terms[key]])
        elif(key == 'gps'):
            cursor.execute("SELECT * FROM inventory WHERE gps = ?", [search_terms[key]])
        elif(key == 'minChildSeat'):
            cursor.execute("SELECT * FROM inventory WHERE maxChildSeat >= ?;", [search_terms[key]])
        elif(key == 'skiRack'):
            cursor.execute("SELECT * FROM inventory WHERE skiRack = ?;", [search_terms[key]])
        elif(key == 'snowChains'):
            cursor.execute("SELECT * FROM inventory WHERE snowChains = ?;", [search_terms[key]])
        elif(key == 'leftControl'):
            cursor.execute("SELECT * FROM inventory WHERE leftControl = ?;", [search_terms[key]])
        elif(key == 'autoTransmission'):
            cursor.execute("SELECT * FROM inventory WHERE autoTransmission = ?;", [search_terms[key]])
        elif(key == 'year'):
            cursor.execute("SELECT * FROM inventory WHERE year = ?;", [search_terms[key]])
    vehicles = cursor.fetchall()
    vehicle_dictionary_array = []
    for vehicle in vehicles:
        vehicle_dictionary = {
            "vehicleID":vehicle[0],
            "make": vehicle[1],
            "model": vehicle[2],
            "year": vehicle[3],
            "location": vehicle[4],
            "cost": vehicle[5],
            "passengers": vehicle[6],
            "autoTransmission": vehicle[7],
            "type": vehicle[8],
            "mpg": vehicle[9],
            "specialEquipment": {
                "gps": vehicle[10],
                "maxChildSeat": vehicle[11],
                "skiRack": vehicle[12],
                "snowChains": vehicle[13],
                "leftControl": vehicle[14]
            }
        }
        vehicle_dictionary_array.append(vehicle_dictionary)
    conn.close()
    if(len(vehicle_dictionary_array) == 0):
        return('404', "No vehicles found")
    else:
        return(('200',vehicle_dictionary_array))


def purchase_vehicle(purchaseInformation):
    vehicleID = purchaseInformation["vehicleID"]
    startDate = purchaseInformation["startDate"]
    endDate = purchaseInformation["endDate"]

    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reservation WHERE vehicleID = ? AND endDate > ? AND startDate < ?", (vehicleID, startDate, endDate))
    conflicts = cursor.fetchall()
    if(len(conflicts) == 0):
        cursor.execute("INSERT INTO reservation VALUES (?,?,?)", (vehicleID, startDate, endDate))
        print("success")
    else:
        print("ERROR:")
        print(conflicts)
    conn.commit()
    conn.close()