# chat_client.py
print("Loading Chat Client...")
import sys, socket, select, os, time
from tkinter import BooleanVar
from tkinter import *
from tkinter import Toplevel
from datetime import datetime
open = False

def timenow():
    return ("[" + datetime.now().strftime('%H:%M:%S') + "]")

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
        
        gf = LabelFrame(self, text = 'General', relief = GROOVE, labelanchor = 'nw', width = 400, height = 90)
        gf.grid(row = 1, column = 1)
        gf.grid_propagate(0)
        Label(gf, text = 'Host:').grid(row = 0, column = 1)
        Entry(gf, textvariable = self.options['host']).grid(row = 0, column = 2, columnspan = 2)
        Label(gf, text = 'Port:').grid(row = 1, column = 1)
        Entry(gf, textvariable = self.options['port']).grid(row = 1, column = 2, columnspan = 2)
        Label(gf, text = 'Nickname:').grid(row = 2, column = 1)
        Entry(gf, textvariable = self.options['nickname']).grid(row = 2, column = 2, columnspan = 2)
        Label(self , text = " Original Code By Samuel Simpson").grid(row = 4, column = 1)
        Button(self, text = "Load Chat", command = self.launch).grid(row = 3, column = 1)

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
        connected = False
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
                    msg.set(c)

                msg.trace("w", lambda name, index, mode, msg=msg: callback(msg))
                entry = Entry(self, textvariable=msg,width = 140)
                entry.grid(row = 1, column = 2)
                entry.bind('<Return>', self.sendmessage)
                df = LabelFrame(self, text = 'Chat')
                df.grid(row = 0, column = 2)
                self.elements['logs'] = Text(df, foreground="white", background="black", highlightcolor="white", highlightbackground="purple", wrap=WORD, height = 25, width = 100)
                self.elements['logs'].grid(row = 0, column = 1)
                Button(self, text = 'Send', command = self.sendmessage).grid(row = 1, column = 3)
                
                
            if not connected:
                
                host = self.options["host"].get()
                port = self.options["port"].get()
        
                globals()["s"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.2)
     
                # connect to remote host
                try :
                    s.connect((host, port))
                    s.send((self.options["nickname"].get()).encode())
                    time.sleep(0.5)
                    s.send((os.getlogin()).encode())
                    time.sleep(0.5)
                    s.send(socket.gethostname().encode())
                    message = 'Connected to remote host. You can start sending messages'
                    message = message + "\n"
                    self.elements['logs'].insert(END, message)
                    self.elements['logs'].yview_moveto(1.0)

                    globals()["readytosend"] = 1
                    connected = True
                    
                except :
                    message = 'Unable to connect'
                    message = message + "\n"
                    self.elements['logs'].insert(END, message)
                    self.elements['logs'].yview_moveto(1.0)
                    time.sleep(2)
                
                def checkformessages():
                    try:
                        data = s.recv(4096)
                        if not data:
                            globals()["disconnected"] = True
                            message = 'Disconnected from server'
                            message = message + "\n"
                            self.elements['logs'].insert(END, message)
                            self.elements['logs'].yview_moveto(1.0)
                            
                        else:
                            message = data.decode() + "\n"
                            self.elements['logs'].insert(END, message)
                            self.elements['logs'].yview_moveto(1.0)
                    except:
                        pass
                    
            if connected:
                checkformessages()

            def sockclose():
                s.close()
                self.destroy()
                
            self.protocol("WM_DELETE_WINDOW", sockclose)
            
            self.update()
                                
    def sendmessage(self, *args):
        if readytosend == 1:
            readytosend == 0
            globals()["msgdata"] = msg.get()
            s.send(msgdata.encode())
            msg.set("")
            readytosend == 1


if __name__ == "__main__":
    print("Done!")
    try:
        MainWindow()
        input()
    except Exception as ex:
        print('There was an error: %s.\nQuitting.' % ex)
        sys.exit()
    

