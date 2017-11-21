import sqlite3

dbAddress = 'app/data_objects/hurts_db.db'

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


    if("startDate" in search_terms.keys() and "endDate" in search_terms.keys() or
           (not("startDate" in search_terms.keys()) and not("endDate" in search_terms.keys()))):
        cursor.execute(
            "SELECT * FROM inventory LEFT OUTER JOIN reservation ON inventory.vehicleID = reservation.vehicleID")
    else:
        #Missing either start or end date query
        return(-1)

    if(len(search_terms) > 0):
        for key in search_terms:
            if(key == "startDate"):
                cursor.execute("SELECT * FROM inventory  WHERE NOT (endDate > ?);", [search_terms[key]])
            elif(key == "endDate"):
                cursor.execute("SELECT * FROM inventory WHERE NOT(startDate < ?);", [search_terms[key]])
            else:
                query = "SELECT * FROM inventory WHERE " + key + "='" + search_terms[key] +"';"
                cursor.execute(query)
    else:
        cursor.execute("SELECT * FROM inventory;")
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
    return(vehicle_dictionary_array)


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