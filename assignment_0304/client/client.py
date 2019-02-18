import sys, os, socket, logging, math
from client_stub import RPCClient
from utils import logger

BUFF_SIZE = 1024
STATIC_DIR = 'static_server/'

if __name__ == "__main__":
    client = RPCClient(('localhost', 8080))
    client.connect_server()
    client.logger = logger

    rpc_client = client.get_rpc_interface()
    rpc_client.add(17,8)
    rpc_client.add(18,8)

    # terminate the connection
    client.disconnect_server()