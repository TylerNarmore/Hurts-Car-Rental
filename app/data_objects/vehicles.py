from redis import Redis

def add_vehicle(vehicle):
    vehicleID = vehicle["vehicleID"]
    quantity = vehicle["quantity"]
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

    #RedisCall
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
    #Use these to search REDIS and return list of vehicles that match
    pass

def purchase_vehicle(vehicleID, startDate, endDate):
    #Set vehicle quantity to 0 in redis
    #Do something to document it was purchased.
    pass



