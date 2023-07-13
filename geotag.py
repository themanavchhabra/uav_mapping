import numpy as np
import math
from haversine import inverse_haversine, Direction

def geotag(sizeX, sizeY, x, y, lat1, lon1, pix2mX, pix2mY, angleUAV):
    center = (sizeX/2, sizeY/2)
    disPix = (center[0] - x, center[1] - y)     # distance from center in pixels

    disKM = ((disPix[0] * pix2mX)/1000, (disPix[1] * pix2mY)/1000) # distance from center in kilometers

    dis = math.sqrt(math.pow(disKM[0],2) + math.pow(disKM[1],2))

    angleImage = math.atan((disPix[0])/(disPix[1]))

    angleTotal = angleUAV + angleImage

    lat2, lon2 = calculate_destination(lat1, lon1, disKM[0], disKM[1])
    lat2, lon2 = inverse_haversine((lat1, lon1), dis, angleTotal)

    return (lat2, lon2)

def calculate_destination(lat1, lon1, disX, disY):

    # Earth's radius in kilometers
    R = 6371.0

    # Convert latitude and longitude to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)

    # Calculate the angular distance traveled along the X-axis (longitude)
    ang_dist_x = disX / (R * math.cos(lat1_rad))

    # Calculate the angular distance traveled along the Y-axis (latitude)
    ang_dist_y = disY / R

    # Calculate the latitude of the second point
    lat2_rad = lat1_rad + ang_dist_y
    lat2 = math.degrees(lat2_rad)

    # Calculate the longitude of the second point
    lon2_rad = lon1_rad + ang_dist_x
    lon2 = math.degrees(lon2_rad)

    return lat2, lon2

def calculate_destination2()

lat2, lon2 = calculate_destination(lat1, lon1, disX, disY)
print("Latitude 2:", lat2)
print("Longitude 2:", lon2)

    
geotag(640, 480, 0, 0, 0, 0, 0, 0)