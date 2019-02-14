import sys, os, socket, logging

logger = logging.getLogger('udp-client')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

address = ('localhost', 8080)
socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

buffer_size = 1024

if __name__ == "__main__":
    socket_client.sendto("hello server!", address)
    try:
        data, server_address_info = socket_client.recvfrom(buffer_size)
        logger.debug("received %s from %s", data, server_address_info)
    except Exception as e:
        print e
    
    
