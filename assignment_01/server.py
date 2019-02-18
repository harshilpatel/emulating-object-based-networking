import sys, os, socket, logging, math

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
STATIC_DIR = 'static_server/'

def serve_file(filename, address):
    filepath = STATIC_DIR + filename
    if not os.path.isfile(filepath):
        logger.debug("file with name %s was not served to %s", filename, address); return False
        
    num_of_packets = os.stat(filepath).st_size/float(BUFF_SIZE) or 1
    num_of_packets = int(math.ceil(num_of_packets))
    socket_server.sendto(str(num_of_packets), address)
    file_to_send = open(filepath, 'r')
    for i in range(num_of_packets):
        data = file_to_send.read(BUFF_SIZE)
        socket_server.sendto(data, address)
    
    file_to_send.close()
    logger.debug("file with name %s was served to %s", filename, address)

def write_file(filename, num_of_packets, address):
    filepath = STATIC_DIR + filename
    file_to_write = open(filepath, 'w+')
    for i in range(num_of_packets):
        data, address = socket_server.recvfrom(BUFF_SIZE)
        file_to_write.write(data)
    
    file_to_write.close()
    logger.debug("file with name %s was read from %s", filename, address)


def rename_file(file_oldname, file_newname):
    file_oldpath = STATIC_DIR + file_oldname
    file_newpath = STATIC_DIR + file_newname
    if(os.path.isfile(file_oldpath)):
        os.rename(file_oldpath, file_newpath)
        return True
    else:
        logger.error("file with name %s was not found", file_oldname)
        return False

def remove_file(filename):
    filepath = STATIC_DIR + filename
    if(os.path.isfile(filepath)):
        os.remove(filepath)
        return True
    else:
        logger.error("file with name %s was not found", filename)
        return False

if __name__ == "__main__":
    while True:
        data, address = socket_server.recvfrom(BUFF_SIZE)
        logger.debug("received a new connection from %s and data %s", address, data)

        request = data.split()
        if request and len(request) > 0:
            cmd, request_content = request[0], request[1]

            if cmd == 'UPLOAD':
                logger.debug("upload request received")
                file_name, num_of_packets = request_content.split(',')
                num_of_packets = int(num_of_packets)
                write_file(file_name, num_of_packets, address)
            if cmd == 'GET':
                logger.debug("static file reqested")
                serve_file(request_content, address)
            if cmd == 'DELETE':
                logger.debug("delete request received")
                remove_file(request_content)
            if cmd == 'RENAME':
                logger.debug("rename request received")
                old_file, new_file = request_content.split(',')
                rename_file(old_file, new_file)
            if cmd == 'ECHO':
                logger.debug("echo request received")
                socket_server.sendto(request_content, address)
                logger.debug("message with text: '%s' echoed back to the socket", request_content)
