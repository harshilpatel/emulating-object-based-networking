import sys, os, socket, logging, math
from client_stub import RPCClient
from utils import logger

BUFF_SIZE = 1024
STATIC_DIR = 'static_server/'

def take_input_matrix(y, x, mat_name):
    result = []

    print "Taking values for %s matrix" % mat_name
    for i in range(y):
        try:
            result.append([int(i) for i in raw_input("Enter space seperate row [%s] for %s matrix: " % (i, mat_name)).split()])
        except ValueError:
            logger.error("failed to read a numeric value")
            return None

    return result

def take_matrix_size(mat_name):
    item_size = raw_input("Enter the %s matrix size like 'Y X': " % mat_name)
    y = x = 0
    
    try:
        item_size = [int(i) for i in item_size.split()]
        y, x = item_size[0], item_size[1]
    except ValueError:
        logger.error("Failed to read a numeric value")
    
    return y, x

if __name__ == "__main__":
    client = RPCClient(('localhost', 8080))
    client.connect_server()
    client.logger = logger

    rpc_client = client.get_rpc_interface()
    logger.debug("Server is connected")

    user_input = ''
    while user_input != '0':
        user_input = raw_input('#'*30 + '\nEnter your action: \n0. Quit, \n1. Calculate Pi, \n2. Add, \n3. Sort, \n4. Matrix Multiply, \nChoice: ')
        if user_input == '1':
            rpc_client.calculate_pi()
        elif user_input == '2':
            first_number = second_number = 0
            try:
                first_number, second_number = float(raw_input("Enter first number: ")), float(raw_input("Enter second number: "))
            except ValueError:
                logger.error("Failed to read a numeric value")

            rpc_client.add(first_number, second_number)
        elif user_input == '3':
            items_list = raw_input("Enter space seperated list like '1 2 3': ")
            items_list = [int(i) for i in items_list.split()]
            rpc_client.sort(items_list)
        elif user_input == '4':
            y1 = x1 = y2 = x2 = 0
            matrix_input_source = ''
            matrixA = []
            matrixB = []
            choice_of_input = raw_input("How would you like to read input: 1.Console 2.File `input.txt`:  ")
            if choice_of_input == '1':
                y1, x1 = take_matrix_size("first")
                y2, x2 = take_matrix_size("second")
            elif choice_of_input == '2':
                matrix_input_source = open('input.txt', 'r')
                y1, x1 = [int(i) for i in matrix_input_source.readline().strip().split()][:2]
                y2, x2 = [int(i) for i in matrix_input_source.readline().strip().split()][:2]
            else:
                continue

            if x1 != y2 or 0 in [y1, x1, y2, x2]:
                logger.error("Cannot multiply for the given size")
                continue
            
            if choice_of_input == '1':
                matrixA = take_input_matrix(y1, x1, "first")
                matrixB = take_input_matrix(y2, x2, "second")
            elif choice_of_input == '2':

                matrix_input = []
                for i in range(y1 + y2):
                    matrix_input.append([int(i) for i in matrix_input_source.readline().split()])

                matrixA = []
                for i in range(y1):
                    matrixA.append(matrix_input[i])
                
                matrixB = []
                for i in range(y2):
                    matrixB.append(matrix_input[y1 + i])
                
                matrix_input_source.close()

            if matrixA and matrixB:
                rpc_client.matrix_multiply(matrixA, matrixB)


    # terminate the connection
    client.disconnect_server()