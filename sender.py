# Angeles, Ma. Mikaela A.
# 201800527
# CS 145 Project

# Import libraries
import sys
import math
import time
import socket
import getopt
import hashlib

# Initialize default variables
ID = '881967a8'
FILE = '881967a8.txt'
ADDR = '10.0.7.141'
RCV_PORT = 9000
SEND_PORT = 6670
HOST_NAME = socket.gethostbyname(socket.gethostname())

# Checksum function
# Given in the project specifications
def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

# Parse user input in the terminal using getopt library
# Source: https://www.geeksforgeeks.org/getopt-module-in-python/
def parse_input(str):
    global FILE, ADDR, RCV_PORT, SEND_PORT, ID
    try:
        flags, args = getopt.getopt(str, "f:a:s:c:i:")
    except:
        return ">> No additional flags found."

    for flag, arg in flags:
        if flag in ['-f']:      # -f denotes the filename of the payload
            FILE = flag
        elif flag in ['-a']:    # -a denotes the IP address of the receiver to be contacted
            ADDR = flag
        elif flag in ['-s']:    # -s denotes the port to be used by the receiver
            RCV_PORT = flag
        elif flag in ['-c']:    # -c denotes the port to be used by the sender
            SEND_PORT = flag
        elif flag in ['-i']:    # -i denotes the unique ID
            ID = flag

    return

def main():
    # Parse the user input in the terminal
    parse_input(sys.argv[1:])

    # Initiate UDP connection
    UDP_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # Initialize the address to be used
    DST_ADDR = (ADDR, SEND_PORT)

    # Bind the UDP socket to host and port
    UDP_SOCKET.bind((HOST_NAME, RCV_PORT))

    # Initiate a transaction and send ID
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), DST_ADDR)

    # Receive packets and print transaction ID
    data, x = UDP_SOCKET.recvfrom(64)
    transactionID = data.decode()
    print(f"Transaction ID: {transactionID}")

if __name__ == "__main__":
    main()