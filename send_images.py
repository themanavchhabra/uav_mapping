import socket
import pickle
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--sender_ip', type=str, default='192.168.1.50', help='Sender IP')
args = parser.parse_args()

ip = args.sender_ip #parser input for sender ip for socket connection

# Set up the socket connection
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender_socket.bind((ip, 9999))  # Replace 'sender_pc_ip' with the actual IP address of the sender PC
sender_socket.listen(1)
print('[INFO] Waiting for a connection...')

# Accept a connection from the receiver PC
receiver_socket, address = sender_socket.accept()
print('[INFO] Receiver connected:', address)

i=0
while True:
    image_fname="data/images/"+str(i)+".jpg"
    image=cv2.imread(image_fname)
    text_fname = "data/uav/"+str(i)+".txt"
    try:
        with open(text_fname, 'r') as file:
            text_message = file.read()
    except Exception as e:
        continue
    if image is not None:


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
        i=i+1
    else:
    	print("NO IMAGE")
    	continue
