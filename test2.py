import socket
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8001)
sock.bind(server_address)

# sock.listen(1)

while True:
    # connection, client_address = sock.accept() # tcp connections
    # data = connection.recv(16)

    data, address = sock.recvfrom(1024)

    print "received"
    print data

    sock.sendto(data, address)

    # connection.sendall(data)