# Angeles, Ma. Mikaela A.
# 201800527
# CS 145 Project

import socket
import hashlib

ID = '881967a8'
HOST = '10.0.1.52'
PORT = 6670
ADDR = (HOST, PORT)

UDP_SOCKET = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
FILE = open('payload.txt')

def checksum(packet):
    return hashlib.md5(packet.encode('utf-8')).hexdigest()

def main():
    UDP_SOCKET.bind(('', PORT))
    UDP_SOCKET.sendto(f'ID{ID}'.encode(), ADDR)

    data, addr = UDP_SOCKET.recvfrom(1024)
    transaction = data.decode()
    print(transaction)

if __name__ == "__main__":
    main()