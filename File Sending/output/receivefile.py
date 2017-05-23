import socket,sys,os,hashlib,codecs             # Import socket module
filecodec = 'cp037'

def filehash(filepath):
    openedFile = codecs.open(filepath,'rb',filecodec)
    readFile = openedFile.read().encode()
    openedFile.close()
    sha1Hash = hashlib.sha1(readFile)
    sha1Hashed = sha1Hash.hexdigest()
    return sha1Hashed
def namehash(strtohash):
    sha1Hash = hashlib.sha1(strtohash.encode())
    sha1Hashed = sha1Hash.hexdigest()
    return sha1Hashed

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
        gotfname = False
        tries = 0
        while not gotfname:
            fnamehash = c.recv(4096).decode()
            c.send("Next".encode())
            fname = c.recv(4096).decode()
            tmphash = namehash(fname)
            tries = tries + 1
            if tmphash == fnamehash:
                c.send("Y".encode())
                gotfname = True
                print("VALID FILENAME")
            elif tries >= 5:
                print("INVALID FILENAME")
                c.send("N".encode())
                print("An error occured when receiving the filename")
                c.close()
            else:
                print("INVALID FILENAME")
                c.send("N".encode())

        umoded = c.recv(4096).decode()
        if umoded == "y":
            umode = True
        else:
            umode = False
        c.send("Begin".encode())
        gotfile = False
        tries = 0
        while not gotfile:
            try:
                os.remove(fname + ".tmp")
            except:
                pass
            flen = int(c.recv(4096).decode())
            c.send("Continue".encode())
            fhash = c.recv(4096).decode()
            f = codecs.open(fname + ".tmp",'wb',filecodec)
            c.send("Ready.".encode())
            print("Recieving file: " + fname)
            print("File Length: " + str(flen) + " Chunk(s)")
            flenc = 0
            while flenc < flen:
                print("Receiving Chunk " + str(flenc + 1) + "...")
                l = c.recv(4096).decode(filecodec)
                if (l):
                    f.write(l)
                flenc = flenc + 1
            f.close()
            print("Done Receiving")
            ofhash = filehash(fname + ".tmp")
            tries = tries + 1
            if ofhash == fhash:
                print("VALID FILE")
                c.send("Y".encode())
                gotfile = True
            elif tries >= 5:
                print("INVALID FILE")
                c.send("N".encode())
                print("An error occured when receiving the file")
                c.close()
            else:
                print("INVALID FILE")
                c.send("N".encode())

        print("Saving File...")
        if umode:
            try:
                os.remove(__file__)
            except:
                pass
        try:
            os.remove(fname)
        except:
            pass
        os.rename(fname + ".tmp", fname)
        print("Done Saving")
        c.send('Thank you for connecting'.encode())
        c.close()
        if umode:
            s.close()
            os.system(fname)
            sys.exit()
    except Exception as ex:
        print("An error occured: " + str(ex))
