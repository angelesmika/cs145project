# Angeles, Ma. Mikaela A.
# 201800527
# CS 145 Project

# Import libraries
import sys
import math
import time
import socket
import hashlib
import argparse

# Checksum function
# Given in the project specifications
def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

# Parse user input in the terminal using argparse library
# Source: https://docs.python.org/3/library/argparse.html
def parse_input(str):
    args = argparse.ArgumentParser()
    args.add_argument("-f", default="881967a8.txt")
    args.add_argument("-a", default="10.0.7.141")
    args.add_argument("-s", default=9000)
    args.add_argument("-c", default=6670)
    args.add_argument("-i", default="881967a8")
    
    cmd = args.parse_args()

    return cmd

def main():
    cmd = parse_input(sys.argv[1:])   # Parse user input in the terminal

    # Initialize variables
    ID = cmd.i
    FILE = cmd.f
    ADDR = cmd.a
    RCV_PORT = int(cmd.s)
    SEND_PORT = int(cmd.c)

    # Print variables
    print(f">> Commands: -i: {ID} | -f: {FILE} | -a: {ADDR} | -s: {RCV_PORT} | -c: {SEND_PORT}")

    UDP_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)    # Initiate UDP connection
    HOST_NAME = socket.gethostbyname(socket.gethostname())          # Get host name

    DST_ADDR = (ADDR, RCV_PORT)                # Initialize the address to be used
    UDP_SOCKET.bind((HOST_NAME, SEND_PORT))    # Bind the UDP socket to host and port

    # Initiate a transaction and send ID
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), DST_ADDR)

    # Receive packets and print transaction ID
    transactionID = UDP_SOCKET.recv(64).decode()
    print(f"Transaction ID: {transactionID}")

if __name__ == "__main__":
    main()