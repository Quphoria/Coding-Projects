# chat_client.py
#Coded by Samuel Simpson
#DO NOT attempt to change this as the server has verification to check that clients are valid
print("Loading Chat Client...")

import pip

def install(package):
    pip.main(['install', '--user', package])

imported = False
tries = 0
while not imported:
    try:
        import socket, importlib
        globals()['websocket'] = importlib.import_module('websocket')

        imported = True
    except Exception as ex:
        print("An error occured when importing websocket: " + str(ex))
        tries += 1
        if tries == 6:
            print("Install Failed.")
            while True:
                pass
        print("Installing websocket... [Try " + str(tries) + "/5]")
        try:
            install('websocket-client')
            import site, imp
            imp.reload(site)
            print("Websocket installed.")
        except Exception as ex:
            print("An error occured when installing websocket-client: " + str(ex))

#EDIT
import sys, select, os, time, hashlib, platform, queue, threading
from tkinter import BooleanVar
from tkinter import *
from tkinter import Toplevel
from datetime import datetime
open = False

def timenow():
    return ("[" + datetime.now().strftime('%H:%M:%S') + "]")

def toMD5(strtohash):
    MD5Hash = hashlib.md5(strtohash).hexdigest() #Convert to MD5 Here
    return(MD5Hash)

globals()["tosend"] = []

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = ".o0O| PyChat |O0o.")
        self.lws = []

        self.options = {
            'host' : StringVar(),
            'port' : IntVar(),
            'nickname' : StringVar(),
            "sendmessage" : int(),
            "firsttime" : BooleanVar(),
        }

        hostname = socket.gethostname()
        username = os.getlogin()
        self.options['host'].set('localhost')
        self.options['port'].set(9009)
        self.options['nickname'].set(hostname + ":" + username)
        self.options["firsttime"].set(True)

        def callback(msg):
            c = msg.get()[0:30]
            outtext = ""
            for letter in c:
                if letter != "\\":
                    outtext = outtext + letter
            msg.set(outtext)

        self.options['nickname'].trace("w", lambda name, index, mode, msg=self.options['nickname']: callback(self.options['nickname']))

        gf = LabelFrame(self, text = 'General', relief = GROOVE, labelanchor = 'nw', width = 400, height = 90)
        gf.grid(row = 1, column = 1)
        gf.grid_propagate(0)
        Label(gf, text = 'Host:').grid(row = 0, column = 1)
        Entry(gf, textvariable = self.options['host'], font="Verdana").grid(row = 0, column = 2, columnspan = 2)
        Label(gf, text = 'Port:').grid(row = 1, column = 1)
        Entry(gf, textvariable = self.options['port'], font="Verdana").grid(row = 1, column = 2, columnspan = 2)
        Label(gf, text = 'Nickname:').grid(row = 2, column = 1)
        Entry(gf, textvariable = self.options['nickname'], font="Verdana").grid(row = 2, column = 2, columnspan = 2)
        Label(self , text = " Original Code By Samuel Simpson").grid(row = 4, column = 1)
        Button(self, text = "Load Chat", command = self.launch).grid(row = 3, column = 1)

        Tk.mainloop(self)

    def launch(self):
        self.options["firsttime"].set(True)
        globals()["readytosend"] = 0
        self.lws.append(ChatWindow('%s:%i' % (self.options.get('host').get(), self.options.get('port').get()),self.options))

class ChatWindow(Toplevel):
    def __init__(self, title, options):
        Toplevel.__init__(self)
        self.title(string = title)
        self.options = options
        globals()["msg"] = StringVar()
        self.elements = {}
        globals()["connected"] = False
        globals()["disconnected"] = False
        while not globals()["disconnected"]:
            if self.options["firsttime"].get():
                self.options["firsttime"].set(False)

                sf = LabelFrame(self, text = 'General', width = 180, height = 138)
                sf.grid(row = 0, column = 1)
                sf.grid_propagate(0)
                Label(sf, text = 'Chat Server: %s:%i' % (options['host'].get(), options['port'].get())).grid(row = 0, column = 1)
                Label(sf, text = 'Nickname: %s' % (options['nickname'].get())).grid(row = 1, column = 1)
                Label(sf , text = "").grid(row = 2, column = 1)
                Label(sf , text = "Original Code").grid(row = 3, column = 1)
                Label(sf , text = "By Samuel Simpson").grid(row = 4, column = 1)

                def callback(msg):
                    c = msg.get()[0:150]
                    outtext = ""
                    for letter in c:
                        if letter != "\\":
                            outtext = outtext + letter
                    msg.set(outtext)

                msg.trace("w", lambda name, index, mode, msg=msg: callback(msg))

                df = LabelFrame(self, text = 'Chat')
                df.grid(row = 0, column = 2)
                self.elements['logs'] = Text(df, foreground="white", background="black", highlightcolor="white", highlightbackground="purple", wrap=WORD, height = 25, width = 100, font="Verdana")
                self.elements['logs'].grid(row = 0, column = 0)
                entry = Entry(df, textvariable=msg,width = 100, font="Verdana")
                entry.grid(row = 1, column = 0)
                entry.bind('<Return>', self.sendmessage)
                Button(df, text = 'Send', command = self.sendmessage).grid(row = 1, column = 1)



                host = self.options["host"].get()
                port = self.options["port"].get()
                #EDIT
                globals()["msgqueue"] = queue.Queue(0)


                # connect to remote host
                def connect():
                    globals()["connected"] = False
                    globals()["disconnected"] = False
                    while not globals()["disconnected"]:
                        try:
                            self.update()
                            def on_message(ws,message):
                                globals()["msgqueue"].put(message)
                            def on_close(ws):
                                print("###socket closed###")
                                if globals()["connected"]:
                                    globals()["disconnected"] = True
                            def on_error(ws, error):
                                print ("Socket Error: " + str(error))
                                if globals()["connected"]:
                                    globals()["disconnected"] = True
                            s = websocket.WebSocketApp("ws://" + str(host) + ":" + str(port) + "/", on_message = on_message, on_close=on_close, on_error=on_error)
                            wst = threading.Thread(target=s.run_forever)
                            wst.daemon = True
                            wst.start()

                            #EDIT
                            conn_timeout = 5
                            while not s.sock.connected and conn_timeout:
                                time.sleep(1)
                                conn_timeout -= 1


                            globals()["s"] = s

                            s.send("cf7bcef89b9cf428535a77d5bdc972c8".encode())
                            time.sleep(0.2)
                            s.send((self.options["nickname"].get()).encode())
                            time.sleep(0.2)
                            s.send("True".encode())
                            time.sleep(0.2)
                            s.send((os.getlogin()).encode())
                            time.sleep(0.2)
                            s.send(platform.node().encode())
                            time.sleep(0.2)
                            message = 'Connected to remote host. You can start sending messages.'
                            message = message + "\n"
                            self.elements['logs'].insert(END, message)
                            self.elements['logs'].yview_moveto(1.0)
                            message = 'Type ~help to view commands.'
                            message = message + "\n"
                            self.elements['logs'].insert(END, message)
                            self.elements['logs'].yview_moveto(1.0)

                            globals()["readytosend"] = 1
                            globals()["connected"] = True


                            while globals()["connected"] and not globals()["disconnected"]:

                                try:
                                    self.update()
                                    if len(globals()["tosend"]) > 0:
                                        global readytosend
                                        if readytosend == 1:
                                            readytosend = 0
                                            globals()["msgdata"] = globals()["tosend"].pop(0)
                                            if msgdata[:6] == "~admin":
                                                try:
                                                    msgdatatmp = msgdata.split(' -', 2)
                                                    globals()["msgdata"] = "~admin -" + msgdatatmp[1] + " -" + toMD5(msgdatatmp[2].encode())
                                                except:
                                                    globals()["msgdata"] = "~admin"
                                            elif msgdata[:9] == "~shutdown" or msgdata[:8] == "~restart":
                                                try:
                                                    msgdatatmp = msgdata.split(' -', 1)
                                                    globals()["msgdata"] = msgdatatmp[0] + " -" + toMD5(msgdatatmp[1].encode())
                                                except:
                                                    globals()["msgdata"] = msgdatatmp[0]
                                            #EDIT
                                            s.send(msgdata.encode())
                                            msg.set("")
                                            readytosend = 1
                                    try:
                                        #EDIT
                                        if not globals()["msgqueue"].empty():
                                            data = globals()["msgqueue"].get()
                                            if not data:
                                                globals()["disconnected"] = True
                                            else:
                                                message = data
                                                self.elements['logs'].insert(END, message.decode("utf-8"))
                                                self.elements['logs'].yview_moveto(1.0)
                                    except Exception as ex:
                                        print("ERR: " + str(ex))
                                except Exception as ex:
                                    print("Error: " + str(ex))

                        except Exception as ex:
                            print("Error: " + str(ex))
                            message = 'Unable to connect'
                            message = message + "\n"
                            self.elements['logs'].insert(END, message)
                            self.elements['logs'].yview_moveto(1.0)
                            self.update()
                            try:
                                del globals()["s"]
                            except:
                                pass

                connect()
                message = 'Disconnected from Server'
                message = message + "\n"
                self.elements['logs'].insert(END, message)
                self.elements['logs'].yview_moveto(1.0)
                self.update()
                try:
                    del globals()["s"]
                    del s
                except Exception as ex:
                    print("errs: " + str(ex))


            def sockclose():
                #EDIT
                try:
                    del globals()["s"]
                except:
                    pass
                self.destroy()

            self.protocol("WM_DELETE_WINDOW", sockclose)

            self.update()

    def sendmessage(self, *args):
        globals()["tosend"].append(msg.get())



if __name__ == "__main__":
    print("Done!")
    try:
        MainWindow()
        input()
    except Exception as ex:
        print('There was an error: %s.\nQuitting.' % ex)
        print("Please contact the server administrator for help.")
        input()
sys.exit()
