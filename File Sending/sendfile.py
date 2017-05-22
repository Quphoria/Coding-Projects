import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.

try:
    gotfile = False
    while not gotfile:
        try:
            print()
            sfile = input("File: ")
            f = open("input/" + sfile,'rb')
            gotfile = True
        except Exception as ex:
            print("An error occured when opening the file: " + str(ex))

    connected = False
    while not connected:
        try:
            s.connect((host, port))
            connected = True
        except Exception as ex:
            print("An error occured when connecting: " + str(ex))

    gotdata = False
    while not gotdata:
        try:
            data = input("Is this file an update[Y/N]? ")
            if data.lower() == "y":
                isupdate = "y"
                gotdata = True
            elif data.lower() == "n":
                isupdate = "n"
                gotdata = True
            else:
                print("Please enter either Y or N")
                print()
        except:
            print("Please enter either Y or N")
            print()


    s.send(sfile.encode())
    s.recv(4096)
    s.send(isupdate.encode())
    print(s.recv(4096).decode())
    print('Sending...')
    l = f.read(4096)
    while (l):
        print('Sending...')
        s.send(l)
        l = f.read(4096)
    f.close()
    s.shutdown(socket.SHUT_WR)
    print ("Done Sending")
    print(s.recv(4096).decode())
    s.close()                     # Close the socket when done
except Exception as ex:
    print("An error occured: " + str(ex))
