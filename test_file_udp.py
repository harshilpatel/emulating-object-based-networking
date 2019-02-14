import sys, os, socket, logging

logger = logging.getLogger('udp-server')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

socket_address = ('localhost', 8080)
socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socket_server.bind(socket_address)

buffer_size = 1024

def serve_file(name, address):
    file_to_send = open(name, 'r')
    data = file_to_send.read(buffer_size)
    while data:
        socket_server.sendto(data, address)
        data = file_to_send.read(buffer_size)
    
    file_to_send.close()
    logger.debug("file with name %s was served to %s", name, address); return True

def write_file(name, data):
    file_to_write = open(name, 'a')
    data, address = socket_server.recvfrom(buffer_size)
    while data:
        socket_server.settimeout(30)
        file_to_write.write(data)
        data, address = socket_server.recvfrom(buffer_size)
    
    file_to_write.close()
    logger.debug("file with name %s was read from %s", name, address); return True


def rename_file(old_name, new_name):
    if(os.path.isfile(old_name)):
        os.rename(old_name, new_name)
        return True
    else:
        logger.error("file with name %s was not found", old_name)
        return False

def remove_file(file_name):
    if(os.path.isfile(file_name)):
        os.remove(file_name)
        return True
    else:
        logger.error("file with name %s was not found", file_name)
        return False

while True:
    data, address = socket_server.recvfrom(buffer_size)
    logger.debug("received a new connection from %s and data %s", address, data)
    socket_server.sendto(data, address)
    logger.debug("data echoed back to the socket")

    request = data.split()
    if request and len(request) > 0:
        cmd, request_type = request[0], request[1]

        if cmd == 'UPLOAD':
            write_file(request_type, address)
        if cmd == 'GET':
            serve_file(request_type, address)
        if cmd == 'DELETE':
            remove_file(request_type)
        if cmd == 'RENAME':
            rename_file(request_type)
        

    
