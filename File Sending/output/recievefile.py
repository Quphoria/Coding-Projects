import socket,sys,os              # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.
bound = False
while not bound:
    try:
        s.bind((host, port))        # Bind to the port
        bound = True
    except Exception as ex:
        print("An error occured when binding the server: " + str(ex))


s.listen(5)                 # Now wait for client connection.
while True:
    try:
        print()
        print("Waiting for connection...")
        c, addr = s.accept()     # Establish connection with client.
        print('Got connection from', addr)
        fname = c.recv(4096).decode()
        c.send("Next".encode())
        umoded = c.recv(4096).decode()
        if umoded == "y":
            umode = True
        elif umoded == "n":
            umode = False
        else:
            raise Exception("Incorrect Update Mode")
        if umode:
            os.remove(__file__)
        f = open("" + fname,'wb')
        c.send("Ready.".encode())
        print("Recieving file: " + fname)
        print("Receiving...")
        l = c.recv(4096)
        while (l):
            print("Receiving...")
            f.write(l)
            l = c.recv(4096)
        f.close()
        print("Done Receiving")
        c.send('Thank you for connecting'.encode())
        c.close()
        if umode:
            s.close()
            os.system(fname)
            sys.exit()
    except Exception as ex:
        print("An error occured: " + str(ex))
