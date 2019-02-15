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

BUFF_SIZE = 1024
STATIC_DIR = 'static/'

def serve_file(name, address):
    name = STATIC_DIR + name
    if(os.path.isfile(name)):
        num_of_packets = os.stat(name).st_size/BUFF_SIZE or 1
        socket_server.sendto(str(num_of_packets), address)
        file_to_send = open(name, 'r')
        for i in range(num_of_packets):
            data = file_to_send.read(BUFF_SIZE)
            socket_server.sendto(data, address)
        
        file_to_send.close()
        logger.debug("file with name %s was served to %s", name, address); return True
    else:
        logger.debug("file with name %s was not served to %s", name, address); return False

def write_file(name, num_of_packets, address):
    name = STATIC_DIR + name
    file_to_write = open(name, 'w+')
    for i in range(num_of_packets):
        data, address = socket_server.recvfrom(BUFF_SIZE)
        file_to_write.write(data)
    
    file_to_write.close()
    logger.debug("file with name %s was read from %s", name, address); return True


def rename_file(old_name, new_name):
    old_name = STATIC_DIR + old_name
    new_name = STATIC_DIR + new_name
    if(os.path.isfile(old_name)):
        os.rename(old_name, new_name)
        return True
    else:
        logger.error("file with name %s was not found", old_name)
        return False

def remove_file(file_name):
    file_name = STATIC_DIR + file_name
    if(os.path.isfile(file_name)):
        os.remove(file_name)
        return True
    else:
        logger.error("file with name %s was not found", file_name)
        return False

if __name__ == "__main__":
    while True:
        data, address = socket_server.recvfrom(BUFF_SIZE)
        logger.debug("received a new connection from %s and data %s", address, data)

        request = data.split()
        if request and len(request) > 0:
            cmd, request_content = request[0], request[1]

            if cmd == 'UPLOAD':
                file_name, num_of_packets = request_content.split(',')
                num_of_packets = int(num_of_packets)
                write_file(file_name, num_of_packets, address)
            if cmd == 'GET':
                serve_file(request_content, address)
            if cmd == 'DELETE':
                remove_file(request_content)
            if cmd == 'RENAME':
                old_file, new_file = request_content.split(',')
                rename_file(old_file, new_file)
            if cmd == 'ECHO':
                socket_server.sendto(request_content, address)
                logger.debug("data echoed back to the socket")
