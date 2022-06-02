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

# Initiate UDP connection and set a timeout
UDP_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDP_SOCKET.settimeout(10)

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

def get_max_payload_size(ID, TID, DEST, payload):
    payloadSize = len(payload)

    # Assume that 10% of the payload can be sent on the first try
    msg_len = max(1, math.ceil(int(payloadSize * 0.90)))

    # While the packet is not being sent, remove 5% of the payload
    # until the maximum acceptable packet size is obtained
    while True:
        msg = payload[idx : msg_len + idx] if idx + msg_len < payloadSize else payload[idx : payloadSize - 1]

        z = 0 if idx + msg_len < payloadSize else 1
        packet = f"ID{ID}SN{str(seq_num).zfill(7)}TXN{TID}LAST{str(z)}{msg}"
        print(f"Message: {packet}")

        # Obtain the checksum of the packet
        CHECKSUM = checksum(packet)

        # Send the packet to the server and check if it returns an error
        # If an error is recorded, decrease msg_len by 5% and try sending
        # the packet again until the server validates the packet
        UDP_SOCKET.sendto(packet.encode(), DEST)
        try:
            ACK = UDP_SOCKET.recv(64).decode()
        except socket.error or socket.timeout:
            msg_len = int(msg_len * 0.95)
            continue

        if ACK[-32:] == CHECKSUM:
            print(f">> Checksums match! Maximum payload size is {msg_len}")
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
    print(f">> Commands: -i: {ID} | -f: {FILE} | -a: {ADDR} | -s: {RCV_PORT} | -c: {SEND_PORT}")

    # Get host name
    HOST_NAME = socket.gethostbyname(socket.gethostname())

    DST_ADDR = (ADDR, RCV_PORT)                # Initialize the address to be used
    UDP_SOCKET.bind((HOST_NAME, SEND_PORT))    # Bind the UDP socket to host and port

    # Initiate a transaction and send ID
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), DST_ADDR)

    # Receive packets and print transaction ID
    TID = UDP_SOCKET.recv(64).decode()
    print(f"Transaction ID: {TID}")

    payload = open(FILE).read()
    msg_len = get_max_payload_size(ID, TID, DST_ADDR, payload)

if __name__ == "__main__":
    main()