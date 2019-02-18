import sys, os, socket, logging, math
from server_stub import RPCServer
from utils import logger

BUFF_SIZE = 1024
STATIC_DIR = 'static_server/'

if __name__ == "__main__":
    server = RPCServer(('localhost', 8080))

    # start server
    server.serve_infinitely()