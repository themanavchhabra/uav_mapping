import cv2
import pickle
import socket
from uav_control import get_vehicle_position, get_vehicle_mode, flyMission, hasMissionStarted, isInAir


# Set up the socket connection
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender_socket.bind(('127.0.0.1', 9999))  # Replace 'sender_pc_ip' with the actual IP address of the sender PC
sender_socket.listen(1)
print('[INFO] Waiting for a connection...')

# Accept a connection from the receiver PC
receiver_socket, address = sender_socket.accept()
print('[INFO] Receiver connected:', address)


# while True:
#     if(isInAir == True):
#         vid = cv2.VideoCapture(0)
#         print("camera on")
#         break
#     else:
#         print("waiting for camera to start")
#         continue
try:
    vid = cv2.VideoCapture(0)
    print("[INFO] Camera started")
except Exception as E:
    print("[INFO] No Camera Input")

while hasMissionStarted:
    # print("yeet")
    # Read the image
    # image_path = '1.png'  # Replace with the actual path to your image file
    # image = cv2.imread(image_path)

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
