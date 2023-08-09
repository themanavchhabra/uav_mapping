from dronekit import connect, VehicleMode, LocationGlobalRelative
from wp_reader import readWaypoints
import time
import math
import cv2
import pickle
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--alti', type=int, default=20, help='Altitude')
parser.add_argument('--vehicle_ip', type=str, default='127.0.0.1:14555', help='Vehicle IP')
parser.add_argument('--waypoints', type=str, default='waypointlist.txt', help='file in which list of waypoints')
args = parser.parse_args()

alti = args.alti #parser input for mission altitude
vehicle_ip = args.vehicle_ip
wp_file = args.waypoints

# Connect to the vehicle
vehicle = connect(vehicle_ip,wait_ready=False)

try:
    vid = cv2.VideoCapture(0)
    print("[INFO] Camera started")
except Exception as E:
    print("[INFO] No Camera Input")

waypoints = readWaypoints(wp_file, alti)
print("Recieved %d waypoints" %len(waypoints))

i = 0

# Function to get the current latitude, longitude, altitude and heading
def get_vehicle_position():
    # Refresh the vehicle's attributes
    
    
    # Get the current latitude, longitude, and altitude
    # lat = vehicle.location.global_frame.lat
    # lon = vehicle.location.global_frame.lon
    # alt = vehicle.location.global_frame.alt
    
    #return lat, lon, alt, heading
    return "%s %s %s %s" %(vehicle.location.global_frame.lat,vehicle.location.global_frame.lon,vehicle.location.global_frame.alt, vehicle.heading)

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
       # time.sleep(1)

    print ("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print (" Waiting for arming...")
        #time.sleep(1)

    print ("Taking off!")
    vehicle.simple_takeoff(targetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print (" Altitude: ", vehicle.location.global_relative_frame.alt)
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=targetAltitude*0.95:
            print ("Reached target altitude")
            break
        # time.sleep(1)

def haversine(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c * 1000

def flyMission(alti):
    global isInAir, hasMissionStarted, i

    arm_and_takeoff(alti)

    for waypoint in waypoints:
        lat, lon, alt, idx = waypoint

        target_location = LocationGlobalRelative(lat, lon, alt)
        vehicle.simple_goto(target_location)

        uav_lat, uav_lon = vehicle.location.global_frame.lat, vehicle.location.global_frame.lon
        remaining_distance = haversine(lat, lon, uav_lat, uav_lon)
        print(remaining_distance)

        while(remaining_distance > 1):
            if(idx > 0 and idx < len(waypoints)):
                vehicle.gimbal.rotate(-90,0,0)
                ret, image = vid.read()
                text_message = get_vehicle_position()

                cv2.imwrite('data/images/'+str(i)+".jpg", image)
                f= open(os.path.join('data/uav/',str(i))+".txt","w+")
                f.write(text_message)
                f.close
                i+=1

            uav_lat, uav_lon = vehicle.location.global_frame.lat, vehicle.location.global_frame.lon
            remaining_distance = haversine(lat, lon, uav_lat, uav_lon)
            # print("Distance to waypoint: {0:.2f} meters".format(remaining_distance))
            # time.sleep(1)
        
        print("[INFO] Reached Waypoint %d" %idx)

flyMission(alti)
