__author__ = "730386714"
import sys
from socket import *

def main():

    #server_name = 'comp431-fa23.cs.unc.edu' # Set server name equal to the course machine the server program will execute on
    server_name = gethostname() # Alternatively set server name equal to local machine
    server_port = int(sys.argv[1] )# Set port number of HTTP server to connect to equal to the command line argument given

    for inp in sys.stdin: # Loop through each line of the standard input. Each line is a separate request
        result = ""

        client_socket = socket(AF_INET, SOCK_STREAM) # Create socket object

        try:
            client_socket.connect((server_name, server_port)) # Create TCP socket to server on the given port
        except:
            print("Connection Error")
            try:
                client_socket.connect(('127.0.0.1', server_port)) # If there is an error creating the socket, try to recover by connecting to the local machine instead
            except:
                exit() # Terminate program if unable to recover
        try:
            client_socket.send(inp.encode())
        except:
            client_socket.close()
            exit() # Terminate program if unable to recover
        try:
            result = client_socket.recv(1024) # Receive the data from the server with a buffer of 1024 since it is just a GET request which shouldn't be too long
        except:
            print("Connection Error")
            try:
                result = client_socket.recv(2048) # If there is an error receiving the data, try to recover by using a buffer twice as large
            except:
                client_socket.close()
                exit() # Terminate program if unable to recover
        print(inp, end='') # Echo the input
        print(result.decode()) # Print out the data, decoded from the sequence of bytes into a string

        client_socket.close() # Close the socket

if __name__ == "__main__":
    main()