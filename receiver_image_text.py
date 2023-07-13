import cv2
import pickle
import socket
import numpy as np
import os

# print("chal gaya")

# Set up the socket connection
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

receiver_socket.connect(('192.168.1.20', 9999))  # Replace 'sender_pc_ip' with the actual IP address of the sender PC

i = 0

while True:
    # Receive the packet
    packet_length_bytes = receiver_socket.recv(4)
    packet_length = int.from_bytes(packet_length_bytes, byteorder='big')

    # Receive the serialized packet data
    serialized_packet = b''
    while len(serialized_packet) < packet_length:
        packet = receiver_socket.recv(packet_length - len(serialized_packet))
        if not packet:
            break
        serialized_packet += packet
    if not serialized_packet:
        raise ValueError('Failed to receive the packet')

    # Deserialize the packet
    packet = pickle.loads(serialized_packet)

    # Extract the image and text from the packet
    serialized_image = packet['image_data']
    text_message = packet['text_message']

    if(serialized_image == None and text_message == "mission_completed"):
        break

    # Deserialize the image
    image = pickle.loads(serialized_image)

    # Display the image
    # cv2.imshow('Received Image', image)
    cv2.imwrite(os.path.join('data/images/',str(i))+'.png', image)

    f= open(os.path.join('data/uav/',str(i))+".txt","w+")
    f.write(text_message)
    f.close
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Print the received text message
    print('Received Text:', text_message)
    i+=1

print("[INFO] Image downlink ended")

# Close the connection
receiver_socket.close()
