import socket,sys,os,hashlib,codecs,time             # Import socket module
#filecodec = 'cp037'
filecodec = None
buffersize = 1024
failed = False


def filehash(filepath):
    openedFile = codecs.open(filepath,'rb',filecodec)
    # readFile = openedFile.read().encode()
    readFile = openedFile.read()
    openedFile.close()
    sha1Hash = hashlib.sha1(readFile)
    sha1Hashed = sha1Hash.hexdigest()
    return sha1Hashed
def namehash(strtohash):
    sha1Hash = hashlib.sha1(strtohash.encode())
    sha1Hashed = sha1Hash.hexdigest()
    return sha1Hashed
def chunkhash(chunktohash):
    sha1Hash = hashlib.sha1(chunktohash)
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
            print("Filename Valid")
        elif tries >= 5:
            print("Filename Invalid")
            c.send("N".encode())
            print("An error occured when receiving the filename")
            c.close()
        else:
            print("Filename Invalid")
            print("Attempting to get the filename again ...")
            print()
            c.send("N".encode())

    umoded = c.recv(buffersize).decode()
    if umoded == "y":
        umode = True
    else:
        umode = False
    c.send("Start".encode())
    exist = False
    gothash = False
    while not gothash:
        cfhash = c.recv(buffersize).decode()
        c.send(cfhash.encode())
        returndata = c.recv(buffersize).decode()
        if returndata == "y":
            gothash = True
    try:
        if cfhash == filehash(fname):
            exist = True
    except:
        pass
    if not exist:
        c.send("n".encode())
        print("File not found or out of date, downloading new version...")
        gotfile = False
        tries = 0
        while not (gotfile or failed):
            try:
                try:
                    os.remove(fname + ".tmp")
                except:
                    pass
                flen = int(c.recv(buffersize).decode())
                c.send("Continue".encode())
                fhash = c.recv(buffersize).decode()
                f = codecs.open(fname + ".tmp",'wb',filecodec)
                c.send("Ready.".encode())
                print("Receiving file: " + fname)
                print("File Length: " + str(flen) + " Chunk(s)")
                flenc = 0
                print()
                while flenc < flen:
                    gotchunk = False
                    while not gotchunk:
                        sys.stdout.write("\rReceiving Chunk " + str(flenc + 1) + "...")
                        # l = c.recv(buffersize).decode(filecodec)
                        l = c.recv(buffersize)
                        lhash = chunkhash(l)
                        c.send(lhash.encode())
                        lvalid = c.recv(buffersize).decode()
                        c.send("RD".encode())
                        if lvalid == "y":
                            gotchunk = True
                        elif lvalid == "n":
                            sys.stdout.write("\rFailed to recieve Chunk " + str(flenc + 1))
                            print()
                        else:
                            sys.stdout.write("\r ")
                            print()
                            failed = True
                            raise(Exception("Failed to recieve Chunk " + str(flenc + 1) ", please try again later."))

                    if (l):
                        f.write(l)
                    flenc = flenc + 1
                f.close()
                print("Done Receiving")
                ofhash = filehash(fname + ".tmp")
                tries = tries + 1
                if ofhash == fhash:
                    print("File Valid")
                    c.send("Y".encode())
                    gotfile = True
                elif tries >= 5:
                    print("File Invalid")
                    c.send("N".encode())
                    print("An error occured when receiving the file")
                    failed = True
                    c.close()
                else:
                    print("File Invalid")
                    print("Attempting to restart the download...")
                    print()
                    c.send("N".encode())
            except Exception as ex:
                try:
                    f.close()
                except:
                    pass
                try:
                    c.send("N".encode())
                except:
                    pass
                    print("An error occured when receiving the file: " + str(ex))
        if not failed:
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
    else:
        c.send("y".encode())
        print("File already exists and is up to date")
    if not failed:
        print(c.recv(buffersize).decode())
        c.close()
        if umode:
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
