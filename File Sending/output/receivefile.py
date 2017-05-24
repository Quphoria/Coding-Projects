import socket,sys,os,hashlib,codecs,time             # Import socket module
filecodec = 'cp037'
buffersize = 4096

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

c = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.
connected = False
while not connected:
    try:
        c.connect((host, port))
        connected = True
    except Exception as ex:
        print("An error occured when connecting: " + str(ex))
        time.sleep(5)


try:

    print('Connected to ', host)
    gotfname = False
    tries = 0
    while not gotfname:
        fnamehash = c.recv(buffersize).decode()
        c.send("Next".encode())
        fname = c.recv(buffersize).decode()
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

    umoded = c.recv(buffersize).decode()
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
        flen = int(c.recv(buffersize).decode())
        c.send("Continue".encode())
        fhash = c.recv(buffersize).decode()
        f = codecs.open(fname + ".tmp",'wb',filecodec)
        c.send("Ready.".encode())
        print("Recieving file: " + fname)
        print("File Length: " + str(flen) + " Chunk(s)")
        flenc = 0
        print()
        while flenc < flen:
            sys.stdout.write("\rReceiving Chunk " + str(flenc + 1) + "...")
            l = c.recv(buffersize).decode(filecodec)
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
    print(c.recv(buffersize).decode())
    c.close()
    if umode:
        s.close()
        os.system(fname)
        sys.exit()
except Exception as ex:
    try:
        c.close()
    except:
        pass
    try:
        f.close()
    except:
        pass
    try:
        os.remove(fname + ".tmp")
    except:
        pass
    print("An error occured: " + str(ex))
input()
