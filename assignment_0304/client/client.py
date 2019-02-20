import sys, os, socket, logging, math
from client_stub import RPCClient
from utils import logger

BUFF_SIZE = 1024
STATIC_DIR = 'static_server/'

def take_input_matrix(y, x, mat_name):
    result = []

    print "Taking values for %s matrix" % mat_name
    for i in range(y):
        result.append([])
        for j in range(x):
            try:
                result[i].append(int(raw_input("Enter value for %s at index [%s][%s]: " % (mat_name, i, j))))
            except ValueError:
                logger.error("failed to read a numeric value")
                return None

    return result

def take_matrix_size(mat_name):
    item_size = raw_input("Enter the %s matrix size with a seperator ',' Y,X: " % mat_name)
    item_size = [int(i) for i in item_size.split(',')]
    y, x = item_size[0], item_size[1]
    return y, x

if __name__ == "__main__":
    client = RPCClient(('localhost', 8080))
    client.connect_server()
    client.logger = logger

    rpc_client = client.get_rpc_interface()
    logger.debug("Server is connected")

    user_input = ''
    while user_input != '0':
        user_input = raw_input('Enter your action: \n\t0. Quit, \n\t1. Calculate Pi, \n\t2. Add, \n\t3. Sort, \n\t4. Matrix Multiply, \nChoice: ')
        if user_input == '1':
            rpc_client.calculate_pi()
        elif user_input == '2':
            first_number = raw_input("Enter first number: ")
            second_number = raw_input("Enter second number: ")
            
            try:
                first_number = float(first_number)
                second_number = float(second_number)
            except ValueError:
                logger.error("Failed to read a numeric value")

            rpc_client.add(first_number, second_number)
        elif user_input == '3':
            items_list = raw_input("Enter the list with a seperator ',' like 1,2,3: ")
            items_list = [int(i) for i in items_list.split(',')]
            rpc_client.sort(items_list)
        elif user_input == '4':
            y1, x1 = take_matrix_size("first")
            y2, x2 = take_matrix_size("second")
            y3, x3 = take_matrix_size("third")

            if y1 != x2 or x2 != x3:
                logger.error("Cannot multiply for the given size")
                continue

            matrixA = take_input_matrix(y1, x1, "first")
            matrixB = take_input_matrix(y2, x2, "second")
            matrixC = take_input_matrix(y3, x3, "third")

            if matrixA and matrixB and matrixC:
                rpc_client.matrix_multiply(matrixA, matrixB, matrixC)


    # terminate the connection
    client.disconnect_server()