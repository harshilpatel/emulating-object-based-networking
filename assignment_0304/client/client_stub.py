from utils import logger
import sys, os, socket, logging, math
import json

BUFF_SIZE = 2048

class BaseClient:
    ''' 
        handles request and responses to server while client is connected
    '''

    def send_request(self, request_data):
        self.socket_client.send(request_data)
    
    def decode_response(self, response):
        return json.loads(response).get('result') or None
    
    def get_response(self):
        response = self.socket_client.recv(BUFF_SIZE)
        data = self.decode_response(response)
        self.log_response(data)
        return data
    
    def log_response(self, data):
        self.logger.debug("response from server %s", data)


class RPCClient(BaseClient):
    def __init__(self, server_address):
        self.server_address = server_address
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_rpc_proxy = RPCProxy(self)
    
    def get_rpc_interface(self):
        return self.server_rpc_proxy
    
    def connect_server(self):
        self.socket_client.connect(self.server_address)
    
    def disconnect_server(self):
        self.socket_client.close()
    
    def call(self, name, *args, **kwargs):
        request_data = json.dumps({'method': name, 'args': args})
        self.send_request(request_data)
        response_data = self.get_response()
        
        return response_data


class RPCProxy:
    ''' 
        this acts like a handler to specifically handle 
        anonymous function calls to be executed on the server
    '''
    
    def __init__(self, client):
        self.client = client
    
    def __getattr__(self, name):
        caller_func = lambda *args, **kwargs: self.client.call(name, *args, **kwargs)
        return caller_func



