import sqlite3
import datetime

dbAddress = 'app/data_objects/hurts_db.db'
valid_query_fields = ['location', 'startDate', 'endDate', 'minPrice', 'maxPrice',
                      'minPassenger', 'make', 'model', 'type',
                      'minMPG', 'gps', 'minChildSeats', 'skiRack', 'snowChains',
                      'leftControl', 'autoTransmission', 'year', 'vehicleID']

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S')
        return(1)
    except ValueError:
        return(-1)


def add_vehicles(vehicles_dictionary):
    vehicles = vehicles_dictionary['vehicles']
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()
    for vehicle in vehicles:
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
            cursor.execute("INSERT INTO inventory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (vehicleID, make, model, year, location, cost, passengers,
                           autoTransmission, type, mpg, gps, maxChildSeat, skiRack,
                           snowChains, leftControl))

        except sqlite3.IntegrityError :
            conn.close()
            return(0)
    conn.commit()
    conn.close()
    return(1)


def reset_vehicles_status():
    #Remove all reservations from system
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservation;")
    conn.commit()
    conn.close()
    return(1)


def delete_vehicle(vehicleID):
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE vehicleID=?", [vehicleID])
    conn.commit()
    conn.close()
    return (1)


def search_reservations(search_terms):
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()

    # Confirm both dates are present or neither dates are present.
    if not ("startDate" in search_terms.keys() and "endDate" in search_terms.keys() or
                (not ("startDate" in search_terms.keys()) and not ("endDate" in search_terms.keys()))):
        return (('400', "Only start date or end date provided"))

    query_string = "SELECT * FROM inventory i INNER JOIN reservation r on r.vehicleID = i.vehicleID"
    if len(search_terms.keys()) == 0:
        pass
    else:
        query_string+=' WHERE '

    first_pass = True
    for key in search_terms:
        if not first_pass:
            query_string += ' AND '
        else:
            first_pass = False
        if not(key in valid_query_fields):
            return(('400', "Invalid query field: "+key))

        if(key == 'location'):
            query_string += "location = '" + search_terms[key] + "'"
        elif(key=='vehicleID'):
            query_string += "i.vehicleID = '" + search_terms[key] + "'"
        elif(key == 'startDate' or key == 'endDate'):
            if(validate(search_terms['startDate'])==1 and validate(search_terms['endDate'])==1):
                if(datetime.datetime.strptime(search_terms['startDate'], '%Y-%m-%dT%H:%M:%S') > datetime.datetime.strptime(search_terms['endDate'], '%Y-%m-%dT%H:%M:%S')):
                    return(('422', "Error: Start date after end date"))
            else:
                return(('422', "Error: Datetime formatted incorrectly"))
            query_string += "EXISTS (SELECT vehicleID FROM reservation r WHERE i.vehicleID = r.vehicleID AND endDate > '" + search_terms['startDate'] + "' AND startDate < '" + search_terms['endDate'] + "')"

        elif(key == 'minPrice'):
            query_string += "cost >= '" + search_terms[key] + "'"
        elif(key == 'maxPrice'):
            query_string += "cost <= '" + search_terms[key] + "'"
        elif(key == 'minPassenger'):
            query_string += "passengers >= '" + search_terms[key] + "'"
        elif(key == 'make'):
            query_string += "make = '" + search_terms[key] + "'"
        elif(key == 'model'):
            query_string += "model = '" + search_terms[key] + "'"
        elif(key == 'type'):
            query_string += "type = '" + search_terms[key] + "'"
        elif(key == 'minMPG'):
            query_string += "mpg >= '" + search_terms[key] + "'"
        elif(key == 'gps'):
            query_string += "gps = '" + search_terms[key] + "'"
        elif(key == 'minChildSeat'):
            query_string += "maxChildSeat >= '" + search_terms[key] + "'"
        elif(key == 'skiRack'):
            query_string += "skiRack = '" + search_terms[key] + "'"
        elif(key == 'snowChains'):
            query_string += "snowChains = '" + search_terms[key] + "'"
        elif(key == 'leftControl'):
            query_string += "leftControl = " + search_terms[key]
        elif(key == 'autoTransmission'):
            query_string += "autoTransmission = " + search_terms[key]
        elif(key == 'year'):
            query_string += "year = '" + search_terms[key] + "'"

    query_string += ";"
    print(query_string)
    cursor.execute(query_string)
    reservations = cursor.fetchall()
    reservations_info_list = []
    for reservation in reservations:
        vehicle_dictionary = {
            "vehicleID": reservation[0],
            "make": reservation[1],
            "model": reservation[2],
            "year": reservation[3],
            "location": reservation[4],
            "cost": reservation[5],
            "passengers": reservation[6],
            "autoTransmission": reservation[7],
            "type": reservation[8],
            "mpg": reservation[9],
            "specialEquipment": {
                "gps": reservation[10],
                "maxChildSeat": reservation[11],
                "skiRack": reservation[12],
                "snowChains": reservation[13],
                "leftControl": reservation[14]
            }
        }
        reservation_dictionary = {
            "startDate": reservation[17],
            "endDate": reservation[16]
        }

        reservations_info_list.append({"vehicleInfo":vehicle_dictionary, "reservationInfo": reservation_dictionary})

    if len(reservations_info_list) == 0:
        return ('404', "No reservations found")
    else:
        return(("200", reservations_info_list))


def find_vehicle(search_terms):
    #Search terms is a dictionary of terms being searched with the category
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()

    #Confirm both dates are present or neither dates are present.
    if not("startDate" in search_terms.keys() and "endDate" in search_terms.keys() or
            (not ("startDate" in search_terms.keys()) and not ("endDate" in search_terms.keys()))):
        return(('400', "Only start date or end date provided"))
    query_string = 'SELECT * FROM inventory i'
    if(len(search_terms.keys()) == 0):
        pass
    else:
        query_string+=' WHERE '

    first_pass = True
    for key in search_terms:
        if not first_pass:
            query_string += ' AND '
        else:
            first_pass = False
        if not(key in valid_query_fields):
            return(('400', "Invalid query field: "+key))

        if(key == 'location'):
            query_string += "location = '" + search_terms[key] + "'"

        elif(key == 'startDate' or key == 'endDate'):
            if(validate(search_terms['startDate'])==1 and validate(search_terms['endDate'])==1):
                if(datetime.datetime.strptime(search_terms['startDate'], '%Y-%m-%dT%H:%M:%S') > datetime.datetime.strptime(search_terms['endDate'], '%Y-%m-%dT%H:%M:%S')):
                    return(('422', "Error: Start date after end date"))
            else:
                return(('422', "Error: Datetime formatted incorrectly"))
            query_string += "NOT EXISTS (SELECT vehicleID FROM reservation r WHERE i.vehicleID = r.vehicleID AND endDate > '" + search_terms['startDate'] + "' AND startDate < '" + search_terms['endDate'] + "')"

        elif(key == 'minPrice'):
            query_string += "cost >= '" + search_terms[key] + "'"
        elif(key == 'maxPrice'):
            query_string += "cost <= '" + search_terms[key] + "'"
        elif(key == 'minPassenger'):
            query_string += "passengers >= '" + search_terms[key] + "'"
        elif(key == 'make'):
            query_string += "make = '" + search_terms[key] + "'"
        elif(key == 'model'):
            query_string += "model = '" + search_terms[key] + "'"
        elif(key == 'type'):
            query_string += "type = '" + search_terms[key] + "'"
        elif(key == 'minMPG'):
            query_string += "mpg >= '" + search_terms[key] + "'"
        elif(key == 'gps'):
            query_string += "gps = '" + search_terms[key] + "'"
        elif(key == 'minChildSeat'):
            query_string += "maxChildSeat >= '" + search_terms[key] + "'"
        elif(key == 'skiRack'):
            query_string += "skiRack = '" + search_terms[key] + "'"
        elif(key == 'snowChains'):
            query_string += "snowChains = '" + search_terms[key] + "'"
        elif(key == 'leftControl'):
            query_string += "leftControl = " + search_terms[key]
        elif(key == 'autoTransmission'):
            query_string += "autoTransmission = " + search_terms[key]
        elif(key == 'year'):
            query_string += "year = '" + search_terms[key] + "'"

    query_string += ";"
    cursor.execute(query_string)
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
        return("200")
    else:
       return(("422", conflicts))
    conn.commit()
    conn.close()