from dronekit import connect, VehicleMode, LocationGlobalRelative
from wp_reader import readWaypoints
import time
import math
import cv2
import pickle
import socket

# Set up the socket connection
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender_socket.bind(('192.168.1.20', 9999))  # Replace 'sender_pc_ip' with the actual IP address of the sender PC
sender_socket.listen(1)
print('[INFO] Waiting for a connection...')


# Accept a connection from the receiver PC
receiver_socket, address = sender_socket.accept()
print('[INFO] Receiver connected:', address)

# Connect to the vehicle
vehicle = connect('127.0.0.1:14555')

try:
    vid = cv2.VideoCapture(0)
    print("[INFO] Camera started")
except Exception as E:
    print("[INFO] No Camera Input")

waypoints = readWaypoints('waypoint_list_smaller.txt')
print("Recieved %d waypoints" %len(waypoints))


isInAir = False
hasMissionStarted = False

# Function to get the current latitude, longitude, altitude and heading
def get_vehicle_position():
    # Refresh the vehicle's attributes
    
    
    # Get the current latitude, longitude, and altitude
    # lat = vehicle.location.global_frame.lat
    # lon = vehicle.location.global_frame.lon
    # alt = vehicle.location.global_frame.alt
    
    #return lat, lon, alt, heading
    return "%s %s %s" %(vehicle.location.global_frame.lat,vehicle.location.global_frame.lat,vehicle.location.global_frame.lat, vehicle.heading)
    

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
        print (" Altitude: ", vehicle.location.global_relative_frame.alt)
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=targetAltitude*0.95:
            print ("Reached target altitude")
            break
        time.sleep(1)

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
    global isInAir, hasMissionStarted

    arm_and_takeoff(alti)

    for waypoint in waypoints:
        lat, lon, alt, idx = waypoint

        target_location = LocationGlobalRelative(lat, lon, alt)
        vehicle.simple_goto(target_location)

        uav_lat, uav_lon = vehicle.location.global_frame.lat, vehicle.location.global_frame.lon
        remaining_distance = haversine(lat, lon, uav_lat, uav_lon)
        print(remaining_distance)

        while(remaining_distance > 1):
            if(idx >1 and idx < len(waypoints)):
                ret, image = vid.read()
                text_message = get_vehicle_position()

                # Convert the image to bytes
                serialized_image = pickle.dumps(image)

                # Get the length of the serialized image
                image_length = len(serialized_image)

                # Define the text message

                # Create a packet containing the image and text
                packet = {
                    'image_data': serialized_image,
                    'text_message': text_message
                }

                # Serialize the packet using pickle
                serialized_packet = pickle.dumps(packet)

                # Get the length of the serialized packet
                packet_length = len(serialized_packet)

                # Send the packet length to the receiver PC
                receiver_socket.sendall(packet_length.to_bytes(4, byteorder='big'))

                # Send the serialized packet to the receiver PC
                receiver_socket.sendall(serialized_packet)

            uav_lat, uav_lon = vehicle.location.global_frame.lat, vehicle.location.global_frame.lon
            remaining_distance = haversine(lat, lon, uav_lat, uav_lon)
            # print("Distance to waypoint: {0:.2f} meters".format(remaining_distance))
            # time.sleep(1)
        
        print("[INFO] Reached Waypoint %d" %idx)

        if(idx == 1):
            hasMissionStarted = True

        if(idx == (len(waypoints) - 1)):
            hasMissionStarted = False

    packet = {
    'image_data': None,
    'text_message': "mission_completed"
    }

    serialized_packet = pickle.dumps(packet)

    # Get the length of the serialized packet
    packet_length = len(serialized_packet)

    # Send the packet length to the receiver PC
    receiver_socket.sendall(packet_length.to_bytes(4, byteorder='big'))

    # Send the serialized packet to the receiver PC
    receiver_socket.sendall(serialized_packet)

    vid.release()
    print("[INFO] Camera Closed")

    # Close the connection
    sender_socket.close()

flyMission(50)

# while True:
# 	print(get_vehicle_position())