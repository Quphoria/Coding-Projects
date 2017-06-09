import socket,hashlib,codecs,sys,time,os               # Import socket module
import tkinter as tk
from tkinter import filedialog
#filecodec = 'cp037'
filecodec = None
buffersize = 1024

so = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.

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

try:
    gotfile = False
    while not gotfile:
        try:
            print()
            #sfile = input("File: ")
            root = tk.Tk()
            root.withdraw()
            sfile = filedialog.askopenfilename(initialdir=os.getcwd())
            f = codecs.open(sfile,'rb',filecodec)
            f.close()
            fnhash = namehash(os.path.basename(sfile))
            fhash = filehash(sfile)
            gotfile = True
        except Exception as ex:
            print("An error occured when opening the file: " + str(ex))
            if sfile == "":
                sys.exit()
    print("File: " + sfile)

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




    bound = False
    while not bound:
        try:
            so.bind((host, port))        # Bind to the port
            bound = True
        except Exception as ex:
            print("An error occured when binding the server: " + str(ex))
            time.sleep(5)


    so.listen(5)                 # Now wait for client connection.
    print("Vending " + os.path.basename(sfile) + " on port " + str(port) + "...")
    while True:
        try:
            print()
            print("Waiting for connection...")
            s, addr = so.accept()     # Establish connection with client.
            print('Got connection from', addr)


            sentfname = False
            tries = 0
            while not sentfname:
                s.send(fnhash.encode())
                s.recv(buffersize)
                s.send(os.path.basename(sfile).encode())
                reply = s.recv(buffersize).decode()
                if reply == "Y":
                    sentfname = True
                else:
                    tries = tries + 1
                    if tries >= 5:
                        raise Exception("Error sending filename.")

            s.send(isupdate.encode())
            s.recv(buffersize)
            gotrchash = False
            while not gotrchash:
                s.send(fhash.encode())
                rchash = s.recv(buffersize).decode()
                if rchash == fhash:
                    s.send("y".encode())
                    gotrchash = True
                else:
                    s.send("n".encode())


            alreadygot = s.recv(buffersize).decode()
            sentfile = False
            tries = 0
            while not (sentfile or alreadygot == "y") :
                f = codecs.open(sfile,'rb',filecodec)
                flen = 0
                l = f.read(buffersize)
                while (l):
                    l = f.read(buffersize)
                    flen = flen + 1
                print(str(flen) + " Chunk(s) Detected")
                f.close()
                s.send(str(flen).encode())
                s.recv(buffersize)
                f = codecs.open(sfile,'rb',filecodec)
                s.send(fhash.encode())
                print(s.recv(buffersize).decode())
                cnum = 0
                l = f.read(buffersize)
                print()
                chunkfails = 0
                while (l):
                    cnum = cnum + 1
                    sentchunk = False
                    while not sentchunk:
                        sys.stdout.write('\rSending Chunk ' + str(cnum) + '...')
                        # s.send(l.encode(filecodec))
                        lhash = chunkhash(l)
                        s.send(l)
                        receivehash = s.recv(buffersize).decode()
                        if receivehash == lhash:
                            chunkfails = 0
                            s.send("y".encode())
                            sentchunk = True
                            s.recv(buffersize)
                        elif chunkfails < 25:
                            chunkfails = chunkfails + 1
                            s.send("n".encode())
                            sys.stdout.write('\rFailed to send Chunk ' + str(cnum))
                            print()
                            s.recv(buffersize)
                        else:
                            s.send("c".encode())
                            sys.stdout.write('\rFailed to send Chunk ' + str(cnum))
                            print()
                            s.recv(buffersize)
                            raise(Exception('Failed to send Chunk ' + str(cnum)))
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
            s.send('Thank you for connecting'.encode())
            s.close()                     # Close the socket when done
        except Exception as ex:
            try:
                s.close()
            except:
                pass
            print("An error occured: " + str(ex))
except Exception as ex:
    try:
        so.close()
    except:
        pass
    print("An error occured: " + str(ex))
input()
