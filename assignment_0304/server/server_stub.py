from utils import logger
import sys, os, socket, math
import json

BUFF_SIZE = 2048

class BaseServer:
    def add(self, i, j):
        return i + j
    def add():
    
     number1 = input("First number: ") 
     number2 = input("\nSecond number: ") 
    
     # Adding two numbers 
     # User might also enter float numbers 
    sum = float(number1) + float(number2) 
        return sum
     # Display the sum 
     # will print value in float 
     #print("The sum of {0} and {1} is {2}" .format(number1, number2, sum))

class RPCServer(BaseServer):
    client_pool = []

    def __init__(self, address):
        self.address = address
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def encode_response(self, result):
        # encoded in json format since the response type is unknown
        return json.dumps({'result': result})
        
    def process_request_data(self, data):
        request_data = ''
        
        try:
            request_data = json.loads(data)
        except ValueError:
            logger.error("no json could be decoded")
            return self.encode_response("ERROR")

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

        logger.info("starting server & listen to packets at %s", self.address)

        while True:
            connection, client_address = self.socket_server.accept()
            logger.debug("received a new connection with address %s", client_address)
            try:
                while True:
                    data = connection.recv(BUFF_SIZE)
                    if not data:
                        break
                    
                    logger.debug("received data: %s from client: %s", data, client_address)
                    result = self.process_request_data(data)
                    connection.send(result)
            finally:
                connection.close()
                logger.debug("closed connection to client with address: %s", client_address)
