import sys, os, socket, logging, math

logger = logging.getLogger('udp-client')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

address = ('localhost', 8080)
socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

BUFF_SIZE = 1024
STATIC_DIR = 'static_client/'


def echo(message):
    socket_client.sendto("ECHO " + message, address)
    data, server_address_info = socket_client.recvfrom(BUFF_SIZE)
    logger.debug("received response %s and is a %s match", data, data==message)

def upload_file(filename):
    filepath = STATIC_DIR + filename
    if not os.path.isfile(filepath):
        logger.error("file with name %s was not found", filename)
        return

    num_of_packets = os.stat(filepath).st_size/float(BUFF_SIZE) or 1
    num_of_packets = int(math.ceil(num_of_packets))
    socket_client.sendto("UPLOAD {0},{1}".format(filename, num_of_packets), address)
    document = open(filepath, 'r')
    for i in range(num_of_packets):
        data = document.read(BUFF_SIZE)
        if not data:
            break
        socket_client.sendto(data, address)
    
    document.close()
    logger.debug("file %s was upload to %s with buffer size", filename, BUFF_SIZE)

def download_file(filename):
    filepath = STATIC_DIR + filename
    socket_client.sendto("GET " + filename, address)
    file_to_write = open(filepath, 'w+')
    num_of_packets, addr = socket_client.recvfrom(BUFF_SIZE)
    for i in range(int(num_of_packets)):
        data, addr = socket_client.recvfrom(BUFF_SIZE)
        file_to_write.write(data)
    
    file_to_write.close()
    logger.debug("file with name %s was read from %s", filename, address)

def rename(old_name, new_name):
    if not old_name or not new_name:
        logger.error("missing names")

    socket_client.sendto("RENAME {0},{1}".format(old_name, new_name), address)
    logger.debug("file %s was requested to be renamed to %s". old_name, new_name)

def delete(filename):
    socket_client.sendto("DELETE {0}".format(filename), address)
    logger.debug("file %s was requested to be deleted", filename)

if __name__ == "__main__":

    # all the methods
    '''
        echo("Hello!!")
        upload_file("test.txt")
        rename("test.txt", "text.txt")
        download_file("text.txt")
        delete("text.txt")
    '''

    action = ''
    while action != "0":
        action = input("Enter your action: \n0. quit\n1.Upload\n2.Rename\n3.Download\n4.Delete")
        if action == "1":
            filename = input("Enter the filename to upload: ")
            upload_file(filename)
        elif action == "2":
            old_name = input("Enter the filename to rename: ")
            new_name = input("Enter the new name: ")
            rename(old_name, new_name)
        elif action == "3":
            filename = input("Enter the filename to download: ")
            download_file(filename)
        elif action == "4":
            filename = input("Enter the filename to delete: ")
            delete(filename)