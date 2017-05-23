import socket,hashlib,codecs               # Import socket module
filecodec = 'cp037'
buffersize = 4096

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.

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

try:
    gotfile = False
    while not gotfile:
        try:
            print()
            sfile = input("File: ")
            f = codecs.open("input/" + sfile,'rb',filecodec)
            f.close()
            fnhash = namehash(sfile)
            fhash = filehash("input/" + sfile)
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
    sentfname = False
    tries = 0
    while not sentfname:
        s.send(fnhash.encode())
        s.recv(buffersize)
        s.send(sfile.encode())
        reply = s.recv(buffersize).decode()
        if reply == "Y":
            sentfname = True
        else:
            tries = tries + 1
            if tries >= 5:
                raise Exception("Error sending filename.")

    s.send(isupdate.encode())
    s.recv(buffersize)
    sentfile = False
    tries = 0
    while not sentfile:
        f = codecs.open("input/" + sfile,'rb',filecodec)
        flen = 0
        l = f.read(buffersize)
        while (l):
            l = f.read(buffersize)
            flen = flen + 1
        print(str(flen) + " Chunk(s) Detected")
        f.close()
        s.send(str(flen).encode())
        s.recv(buffersize)
        f = codecs.open("input/" + sfile,'rb',filecodec)
        s.send(fhash.encode())
        print(s.recv(buffersize).decode())
        cnum = 0
        l = f.read(buffersize)
        while (l):
            cnum = cnum + 1
            print('Sending Chunk ' + str(cnum) + '...')
            s.send(l.encode(filecodec))
            l = f.read(buffersize)
        f.close()
        #s.shutdown(socket.SHUT_WR)
        print ("Done Sending")
        result = s.recv(buffersize).decode()
        tries = tries + 1
        if result == "Y":
            sentfile = True
        elif tries >= 5:
                raise Exception("Error sending file.")
    print(s.recv(buffersize).decode())
    s.close()                     # Close the socket when done
except Exception as ex:
    try:
        s.close()
    except:
        pass
    print("An error occured: " + str(ex))
