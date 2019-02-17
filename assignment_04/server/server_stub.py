import sys, os, socket, logging, math
import json

BUFF_SIZE = 2048

class BaseServer:
    def add(self, i, j):
        return i + j

class RPCServer(BaseServer):
    client_pool = []
    logger = None

    def __init__(self, address):
        self.address = address
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def encode_response(self, result):
        # encoded in json format since the response type is unknown
        return json.dumps({'result': result})
        
    def process_request_data(self, data):
        request_data = json.loads(data)
        request_method = request_data['method']
        request_args = request_data['args']
        # request_args_extra = request_data['args_extra']

        requested_func = getattr(self, request_method)
        if callable(requested_func):
            result = requested_func(*request_args)
            return self.encode_response(result)
        else:
            return self.encode_response("Not callable")
    
    def serve_infinitely(self):
        self.socket_server.bind(self.address)
        self.socket_server.listen(1)
        while True:
            connection, client_address = self.socket_server.accept()
            try:
                while True:
                    data = connection.recv(BUFF_SIZE)
                    if not data:
                        break

                    result = self.process_request_data(data)
                    connection.send(result)
            finally:
                connection.close()