__author__ = "730386714"

import sys
import os
from socket import *

def main():

    server_port = int(sys.argv[1]) # Set port number of HTTP server to connect to equal to the command line argument given
    server_socket = socket(AF_INET, SOCK_STREAM) # Create socket object
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Allow reusing the same port after terminating server
    try:
        server_socket.bind(('', server_port)) # Create TCP welcoming socket on the given port
    except:
        print("Connection Error")
        exit() # Terminate if attempt to create socket was unsuccessful
    while True:
        server_socket.listen(1) # Begin listening for TCP requests
        try:
            connection_socket, addr = server_socket.accept() # Accept incoming connection request, creating socket
        except:
            print("Connection Error")
            exit() # Terminate if connection is not able to be accepted
        print("Client Connected to our HTTP Server")
        inp = connection_socket.recv(1024).decode() # Read bytes from the socket and decode them into a string
        result = "" # Create variable to store the result
        # Split up the input
        parsed = []
        a = 0
        b = -1
        for c in range(1, len(inp)):
            if not inp[c].isspace():
                if a < b:
                    parsed.append(inp[a:b+1].strip()) # Creates sections starting at the first character of a word and ending right before the start of a new word, and strips off the whitespace
                    a = c
            else: b = c
        parsed.append(inp[a:len(inp)].strip()) # Creates last section


        if checkGetMethod(parsed,inp) == False: # Checks Get Method token
            result += "ERROR -- Invalid Method token."

        elif checkRequestURL(parsed) == False: # Checks RequestURL token
            result += "ERROR -- Invalid Absolute-Path token."

        elif checkHTTPVersion(parsed) == False: # Checks HTTP-Version token
            result += "ERROR -- Invalid HTTP-Version token."

        elif checkSpuriousText(parsed) == False: # Checks Spurious Text after HTTP-Version token
            result += "ERROR -- Spurious token before CRLF."

        else: # Execute all of the below if the input is valid
            result += "Method = " + parsed[0]
            result += "\nRequest-URL = " + parsed[1]
            result += "\nHTTP-Version = " + parsed[2]
        
            if parsed[1].lower().endswith(".txt") or parsed[1].lower().endswith(".htm") or parsed[1].lower().endswith(".html"): # Checks if RequestURL is a txt, htm, or html file
                cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
                if os.path.exists(cwd + parsed[1]): # Checks if the file exists before trying to open it
                    try:
                        file = open(cwd + parsed[1], "r") # Open the file for reading
                        for line in file:
                            result += "\n" + line.strip() # Print each line of the file one at a time
                        file.close()
                    except Exception: # Catch all other errors here
                        result += f"\nERROR: [Errno 2] No such file or directory: {cwd + parsed[1]}"
                else:
                    result += f"\n404 Not Found: {parsed[1]}" # Error message for if the file does not exist
            else: result += f"\n501 Not Implemented: {parsed[1]}" # Error message for if the file is not a txt, htm, or html file
        connection_socket.send(result.encode()) # Send the result to the client as a sequence of bytes
        connection_socket.close() # Close the connection to this client, but not the welcoming socket

def checkGetMethod(parsed,inp):
    if inp.startswith("G") == False: # Rejects input with whitespace before the GET method token
        return False
    if len(parsed) > 0:
        if parsed[0] == "GET":
            return True
    return False # Rejects input with anything other than "GET" for the GET method token

def checkRequestURL(parsed):
    if len(parsed) > 1: # Makes sure there is at least a RequestURL token
        if parsed[1].startswith("/") == True: # Checks that the token starts with a "/"
            for character in parsed[1]: # Loops through all characters in the token and ensures that they each are one of the acceptable types of symbols
                if (character.isdigit()) == False and (character.isalpha()) == False and (character == ".") == False and (character == "_") == False and (character == "/") == False:
                    return False
            return True
    return False

def checkHTTPVersion(parsed):
    if len(parsed) > 2: # Makes sure there is at least an HTTP-Version token
        if parsed[2].startswith("HTTP/") == True: # Checks that the token starts with an "HTTP/"
            version = parsed[2].split("/") # Splits the token at the "/" to check that there is only one "/" present
            if len(version) == 2:
                versionDigits = version[1].split(".") # Splits the version number at the "." to check that there is only one "." present
                if len(versionDigits) == 2 and versionDigits[0].isdigit() and versionDigits[1].isdigit():
                    return True # Accepts input only if both sides of the "." contain at least one digit, and there is only one "/" and one "." in the token
    return False

def checkSpuriousText(parsed):
    if len(parsed) > 3: # Checks to see if there are more sections in the input after the HTTP-Version token
        for x in range(3, len(parsed)): # Loops through each additional section and strips off the whitespace
            if (parsed[x].strip() != ""):
                return False # Reject the input if an additional section is not empty after stripping the whitespace
    return True

if __name__ == "__main__":
    main()