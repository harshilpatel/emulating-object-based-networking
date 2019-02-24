from utils import logger
import sys, os, socket, math
import json

BUFF_SIZE = 2048

class BaseServer:
    # contains all the methods exposed as RPC callable methods
    def add(self, i, j):
        return i + j
    
    def calculate_pi(self):
        return 3.14
    
    def sort(self, items_list):
        if not items_list:
            logger.error("submitted array for sorting is empty")

        items_list.sort()

        logger.debug("submitted array was sorted to %s", items_list)
        return items_list

    def base_matrix_muliply(self, matrixA, matrixB):
        logger.debug("multiplying matrices: %s and %s", matrixA, matrixB)
        if not matrixA or not matrixB:
            return []
        result = []

        x1 = len(matrixA[0])
        y1 = len(matrixA)

        x2 = len(matrixB[0])
        y2 = len(matrixB)

        for i in range(y1):
            result.append([])
            for j in range(x2):
              result[i].append(0)
            
        for i in range(y1):
            for j in range(x2):
                result[i][j] = 0
                for a in range(y2):
                        result[i][j] += (matrixA[i][a] * matrixB[a][j])
        
        logger.debug("result is %s", result)
        return result

    def matrix_multiply(self, matrixA, matrixB):
        logger.debug("multiplying matrices: %s and %s", matrixA, matrixB)
        result = self.base_matrix_muliply(matrixA, matrixB)

        logger.debug("final result is %s", result)
        return result


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
            logger.info("received a new connection with address %s", client_address)
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
                logger.info("closed connection to client with address: %s", client_address)
