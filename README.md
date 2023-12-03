# HTTP-Client-and-Server
HTTPclient and HTTPserver, two python programs created for the course Internet Services and Protocols at UNC-Chapel Hill.

These programs are meant to simulate the software used by clients and servers when making TCP connections to each other through HTTP.

# Running these programs

These programs can be run on one computer without being modified.

First, use a terminal to start HTTPserver.py with a single command line argument - the number of the port that you would like the server to listen on.

For example, "python HTTPserver.py 5013".

Next, in a different terminal, start HTTPclient.py with the same command line argument, to connect on that same port number.

For example, "python HTTPclient.py 5013".

The server program should output the message "Client Connected to our HTTP Server" if the connection was made successfully.

In the client terminal, input the HTTP GET request in the form "GET [request-url] HTTP/[version-number]". 

Replace [request-url] with a file path beginning with "/" that uses the directory containing HTTPserver.py as the base directory.

For example, the request-url "/files/hello.txt" is valid and will print the contents of the file hello.txt into the client terminal output.

RequestURL must be a txt, htm, or html file.

Replace [version-number] with two numbers separated by a period.

For example, the version-numbers "1.1" and "44.28" are valid. This is just a part of the GET request parser and doesn't affect the actual program or connection in any way.


If you would like to run these programs on separate computers, the HTTPclient program must be modified.

These two lines at the beginning of the program:

	#server_name = 'comp431-fa23.cs.unc.edu'
	server_name = gethostname()

Should be changed to look like this:

	server_name = '[IP-address of server machine]'
	#server_name = gethostname()

Replace [IP-address of server machine] with the IP address of the server machine, including the quotes surrounding it as shown above. Alternatively, you can replace it with the name of the domain name of the server machine, like 'comp431-fa23.cs.unc.edu' for example.

Then, just run the server program on the server machine and the client program on any other machine like usual.
