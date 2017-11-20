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
    #Call redis to reset all vehicles back to their default.
    #AKA set quantity back to 1 and startDate and endDate to nothing
    pass


def delete_vehicle(vehicleID):
    #Check if vehicle exists
    #Delete if it does and return a good message, return bad message if it doesn't
    pass


def find_vehicle(search_terms):
    #Search terms is a dictionary of terms being searched with the category
    conn = sqlite3.connect(dbAddress)
    cursor = conn.cursor()
    if(len(search_terms) > 0):
        for key in search_terms:
            query = "SELECT * FROM inventory WHERE " + key + "='" + search_terms[key] +"';"
            cursor.execute(query)
    else:
        cursor.execute("SELECT * FROM inventory;")
    vehicles = cursor.fetchall()
    conn.close()
    return(vehicles)


def purchase_vehicle(purchaseInformation):
    #Set vehicle quantity to 0 in redis
    #Do something to document it was purchased.
    pass