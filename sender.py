# Angeles, Ma. Mikaela A.
# 201800527
# CS 145 Project

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

    # Bind the UDP socket to host and port
    UDP_SOCKET.bind((HOST_NAME, PORT))

    # Initiate a transaction and send ID
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), DST_ADDR)

    # Receive packets and print transaction ID
    data, addr = UDP_SOCKET.recvfrom(1024)
    transactionID = data.decode()
    print(f"Transaction ID: {transactionID}")

    # Load and read the payload from file
    payload = FILE.read()
    payloadSize = len(payload)

    idx = 0
    seqNum = 0
    msgLen = max(1, payloadSize // 90)

    while idx < payloadSize:
        last = 0 if idx + msgLen < payloadSize else 1
        while True:
            msg = payload[idx:payloadSize-1] if idx + msgLen == payloadSize else payload[idx:idx + msgLen]
            packet = f'ID{ID}SN{str(seqNum).zfill(7)}TXN{transactionID}Z{str(last)}{msg}'

            UDP_SOCKET.sendto(packet.encode(), DST_ADDR)
            print(f"Packet sent:{packet}")

            data, addr = UDP_SOCKET.recvfrom(1024)
            ACK = data.decode()
            print(f"Checksum: {ACK}")

            CHECKSUM = checksum(packet)
            if ACK == CHECKSUM:
                print(">> Checksums match!")
                break
        
        seqNum += 1
        idx += msgLen
        print()

if __name__ == "__main__":
    main()