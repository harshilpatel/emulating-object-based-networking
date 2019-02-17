import sys, os, socket, logging, math
from server_stub import RPCServer

logger = logging.getLogger('udp-server')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

BUFF_SIZE = 1024
STATIC_DIR = 'static_server/'

if __name__ == "__main__":
    server = RPCServer(('localhost', 8080))
    server.logger = logger
    server.serve_infinitely()