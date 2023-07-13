from dronekit import connect, VehicleMode, LocationGlobalRelative
from wp_reader import readWaypoints
import time

waypoints = readWaypoints('waypointlist.txt')
print("Recieved %d waypoints" %len(waypoints))

# Connect to the vehicle
vehicle = connect('192.168.1.66:14555')

isInAir = False
hasMissionStarted = False

# Function to get the current latitude, longitude, and altitude
def get_vehicle_position():
    # Refresh the vehicle's attributes
    
    
    # Get the current latitude, longitude, and altitude
    lat = vehicle.location.global_frame.lat
    lon = vehicle.location.global_frame.lon
    alt = vehicle.location.global_frame.alt
    
    #return lat, lon, alt
    return "%s %s %s" %(lat,lon,alt)
    

def get_vehicle_mode():    
    return str(vehicle.mode)[12:]

def arm_and_takeoff(targetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print (" Waiting for vehicle to initialise...")
        time.sleep(1)

    print ("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print (" Waiting for arming...")
        time.sleep(1)

    print ("Taking off!")
    vehicle.simple_takeoff(targetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print (" Altitude: "), vehicle.location.global_relative_frame.alt
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=targetAltitude*0.95:
            print ("Reached target altitude")
            break
        time.sleep(1)

def flyMission(alti):
    global isInAir, hasMissionStarted

    arm_and_takeoff(alti)

    for waypoint in waypoints:
        lat, lon, alt, idx = waypoint

        target_location = LocationGlobalRelative(lat, lon, alt)
        vehicle.simple_goto(target_location)

        remaining_distance = target_location.distance_to(vehicle.location.global_relative_frame)

        while(remaining_distance > 1):
            print("Distance to waypoint: {0:.2f} meters".format(remaining_distance))
            time.sleep(1)
        
        print("[INFO] Reached Waypoint %d" %idx)

        if(idx == 0):
            hasMissionStarted = True
        if(idx == len(waypoints - 1)):
            hasMissionStarted = False



# while True:
# 	print(get_vehicle_position())