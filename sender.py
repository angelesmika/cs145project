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

# Set timeout
timeout = 0.5

# Initiate UDP connection
UDP_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Checksum function
# Given in the project specifications
def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

# Parse user input in the terminal using argparse library
# Source: https://docs.python.org/3/library/argparse.html
def parse_input():
    args = argparse.ArgumentParser()
    args.add_argument("-f", default="881967a8.txt")
    args.add_argument("-a", default="10.0.7.141")
    args.add_argument("-s", default=9000)
    args.add_argument("-c", default=6670)
    args.add_argument("-i", default="881967a8")
    
    cmd = args.parse_args()

    return cmd

def get_payload_size(ID, TID, DEST, payload):
    payload_len = len(payload)

    # Assume that 10% of the payload can be sent at first try
    # and set the socket timeout to 0.5 seconds
    msg_len = max(1, math.ceil(payload_len * 0.10))
    UDP_SOCKET.settimeout(timeout)

    while True:
        print(F"\nMessage length: {msg_len}")
        msg = payload[0:msg_len]

        packet = f"ID{ID}SN0000000TXN{TID}LAST0{msg}"
        print(f"Message: {packet}")

        # Send the packet to the server and if an error is returned,
        # reduce payload size by 15% until it is accepted
        start = time.time()
        UDP_SOCKET.sendto(packet.encode(), DEST)
        try:
            if msg_len == 0:
                UDP_SOCKET.settimeout(60)

            print(f"CHECKSUM OF SENT:\t{checksum(packet)}")
            ACK = UDP_SOCKET.recv(64).decode()
            print(f"ACK RECEIVED:\t\t{ACK}")
            break
        except socket.error:
            msg_len = int(msg_len * 0.85)
        
    end = time.time()
    processing_interval = end - start
    print(f"Packet send duration: {processing_interval}")

    print(f">> {msg_len} characters can be sent per run!")
    print("\n---\n")
    print(f"(1)\tPACKET SENT: {packet} \t ({msg_len}/{payload_len})")
    
    return msg_len, processing_interval

def main():
    cmd = parse_input()   # Parse user input in the terminal

    # Initialize variables
    ID = cmd.i
    FILE = cmd.f
    ADDR = cmd.a
    RCV_PORT = int(cmd.s)
    SEND_PORT = int(cmd.c)

    # Print variables
    print(f'''========================
    -i: {ID}
    -f: {FILE}
    -a: {ADDR}
    -s: {RCV_PORT}
    -c: {SEND_PORT}
========================\n''')

    # Get host name
    HOST_NAME = socket.gethostbyname(socket.gethostname())

    DST_ADDR = (ADDR, RCV_PORT)                # Initialize the address to be used
    UDP_SOCKET.bind((HOST_NAME, SEND_PORT))    # Bind the UDP socket to host and port

    # Start timer
    start = time.time()

    # Initiate a transaction and send ID
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), DST_ADDR)

    # Receive packets and print transaction ID
    TID = UDP_SOCKET.recv(64).decode()
    print(f"Transaction ID: {TID}")

    # Open the payload file and print the payload size
    payload = open(FILE).read()
    payload_len = len(payload)
    print(f"Total payload size: {payload_len}")

    # Compute for an acceptable payload size (not necessarily the maximum)
    msg_len, processing_interval = get_payload_size(ID, TID, DST_ADDR, payload)

    i = 2           # Packet counter
    SN = 1          # Sequence number
    idx = msg_len   # Index to be accessed in the payload

    UDP_SOCKET.settimeout(processing_interval + 2)  # Account for delay
    while idx < payload_len:
        # Get the (cumulative) length of the payload sent
        sent = idx + msg_len if idx + msg_len < payload_len else payload_len - 1

        # Get the part of the payload to be sent
        msg = payload[idx:idx+msg_len] if idx + msg_len < payload_len else payload[idx:]
        
        # Format the packet to be sent
        Z = 0 if idx + msg_len < payload_len else 1
        packet = f"ID{ID}SN{str(SN).zfill(7)}TXN{TID}LAST{Z}{msg}"
        
        # Send the packet to the server and print
        UDP_SOCKET.sendto(packet.encode(), DST_ADDR)
        try:
            ACK = UDP_SOCKET.recv(64).decode()
        except socket.error:
            print(">> Unexpected error occurred! Terminating...")
            break

        if ACK[-32:] == checksum(packet):
            print(f"({i})\tPACKET SENT: {packet} \t ({sent if Z == 0 else sent + 1}/{payload_len})")

        i += 1
        SN += 1
        idx += msg_len

    # End timer
    end = time.time()

    print("\n=====================================================================")
    print(f"Transaction with ID {TID} terminated! Time elapsed: {round((end - start), 3)}")
    print("=====================================================================")

if __name__ == "__main__":
    main()