# Angeles, Ma. Mikaela A.
# 201800527
# CS 145 Project

import sys
import math
import time
import socket
import hashlib

# Initialize variables
ID = '881967a8'
HOST = '10.0.7.141'
PORT = 6670
SRC_ADDR = (HOST, PORT)
DST_ADDR = (HOST, 9000)
HOST_NAME = socket.gethostbyname(socket.gethostname())

# Initiate UDP connection
UDP_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# Open payload.txt
FILE = open('881967a8.txt')

# Checksum function
def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

# Initialize main function
def main():
    # Print the arguments passed from the command line
    print(f"> Number of arguments: {len(sys.argv)}")

    for arg in sys.argv:
        print("> " + arg)

    # Bind the UDP socket to host and port
    UDP_SOCKET.bind((HOST_NAME, PORT))

    # Set a timeout for the socket
    UDP_SOCKET.settimeout(10)

    # Initiate a transaction and send ID
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), DST_ADDR)

    # Receive packets and print transaction ID
    data, addr = UDP_SOCKET.recvfrom(64)
    transactionID = data.decode()
    print(f"Transaction ID: {transactionID}")

    # Load and read the payload from file
    payload = FILE.read()
    payloadSize = len(payload)
    print(f"> Payload size: {payloadSize}")

    idx = 0
    seqNum = 0
    msgLen = max(1, math.ceil(payloadSize / 90))

    for i in range(0, payloadSize):
        start = time.time()

        while True:
            print(F"> Message length: {msgLen}")
            last = 0 if idx + msgLen < payloadSize else 1

            msg = payload[idx:idx+msgLen] if idx + msgLen < payloadSize else payload[idx:]
            packet = f"ID{ID}SN{str(seqNum).zfill(7)}TXN{transactionID}LAST{str(last)}{msg}"
            
            CHECKSUM = checksum(packet)

            UDP_SOCKET.sendto(packet.encode(), DST_ADDR)
            try:
                ACK = UDP_SOCKET.recv(64).decode()
                print(f"Packet sent: {packet}")
            except socket.error:
                msgLen = int(msgLen * 0.90)
            
            if ACK[-32:] == CHECKSUM:
                print(">> Checksums match!")
                break
        
        end = time.time()
        UDP_SOCKET.settimeout(end - start + 5)

        seqNum += 1
        idx += msgLen
        print()

        if i == 0:
            msgLen = math.ceil(int((start - end) * payloadSize / 90))
            msgLen += msgLen // ((payloadSize // msgLen) - 5)

if __name__ == "__main__":
    main()