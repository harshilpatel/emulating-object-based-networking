import sys, os, socket, logging, math
from client_stub import RPCClient

logger = logging.getLogger('udp-server')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

BUFF_SIZE = 1024
STATIC_DIR = 'static_server/'

if __name__ == "__main__":
    client = RPCClient(('localhost', 8080))
    client.connect_server()
    client.logger = logger

    rpc_client = client.get_rpc_interface()
    rpc_client.add(17,8)

    # terminate the connection
    client.disconnect_server()