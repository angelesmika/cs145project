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
timeout = 10

# Initiate UDP connection and set a timeout
UDP_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDP_SOCKET.settimeout(timeout)

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

def get_max_payload_size(ID, TID, DEST, payload, start):
    payload_size = len(payload)
    
    # Assume that 10% of the payload can be sent on the first try
    msg_len = max(1, math.ceil(payload_size // 10))

    # While the packet is not being sent, remove 10% of the payload
    # until the maximum acceptable packet size is obtained
    while True:
        print(F"\nMessage length: {msg_len}")
        msg = payload[0:msg_len]

        packet = f"ID{ID}SN0000000TXN{TID}LAST0{msg}"
        print(f"Message: {packet}")

        # Send the packet to the server and check if it returns an error
        # If an error is returned, decrease msg_len by 10% and try sending
        # the packet again until the server validates the packet
        UDP_SOCKET.sendto(packet.encode(), DEST)
        try:
            ACK = UDP_SOCKET.recv(64).decode()
        except socket.error:
            msg_len = int(msg_len * 0.90)
            continue
        
        # Check if the packet is valid
        if ACK[-32:] == checksum(packet):
            print(f">> Checksums match! {msg_len} characters can be sent per run!")

            end = time.time()
            print(f"Time elapsed: {round((end - start), 3)}")

            print("\n---\n")

            print(f">> PACKET SENT: {packet} \t ({msg_len}/{payload_size})")
            break

    return msg_len

def main():
    cmd = parse_input(sys.argv[1:])   # Parse user input in the terminal

    # Initialize variables
    ID = cmd.i
    FILE = cmd.f
    ADDR = cmd.a
    RCV_PORT = int(cmd.s)
    SEND_PORT = int(cmd.c)

    # Print variables
    print(f"[ -i: {ID} | -f: {FILE} | -a: {ADDR} | -s: {RCV_PORT} | -c: {SEND_PORT} ]\n")

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

    payload = open(FILE).read()
    payload_size = len(payload)
    print(f"Total payload size: {payload_size}")

    msg_len = get_max_payload_size(ID, TID, DST_ADDR, payload, start)

    SN = 1
    idx = msg_len
    while idx < payload_size:
        # Get the (cumulative) length of the payload sent
        sent = idx + msg_len if idx + msg_len < payload_size else payload_size - 1

        # Get the part of the payload to be sent
        msg = payload[idx:sent]
        
        # Format the packet to be sent
        Z = 0 if idx + msg_len < payload_size else 1
        packet = f"ID{ID}SN{str(SN).zfill(7)}TXN{TID}LAST{Z}{msg}"
        
        # Send the packet to the server and print
        UDP_SOCKET.sendto(packet.encode(), DST_ADDR)
        try:
            ACK = UDP_SOCKET.recv(64).decode()
        except socket.error:
            break

        if ACK[-32:] == checksum(packet):
            print(f">> PACKET SENT: {packet} \t ({sent if Z == 0 else sent + 1}/{payload_size})")

        SN += 1
        idx += msg_len

    # End timer
    end = time.time()

    print("\n=====================================================================")
    print(f"Transaction with ID {TID} terminated! Time elapsed: {round((end - start), 3)}")
    print("=====================================================================")

if __name__ == "__main__":
    main()