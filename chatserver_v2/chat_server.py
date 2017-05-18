# chat_server_v2.py
from datetime import datetime
print(str("[" + datetime.now().strftime('%H:%M:%S') + "] "))
print("")
import threading, sys
global chatserveruser_halt
chatserveruser_halt = 0
def ChatServerUser():
    print("[ChatServerUser] Loading...")
    #EDIT
    import sys, select, os, time, platform, asyncio
    import pip

    def install(package):
        pip.main(['install', '--user', package])
    imported = False
    tries = 0
    while not imported:
        try:
            import socket, importlib
            globals()['websockets'] = importlib.import_module('websockets')

            imported = True
        except Exception as ex:
            print("An error occured when importing websockets: " + str(ex))
            tries += 1
            if tries == 6:
                print("Install Failed.")
                while True:
                    pass
            print("Installing websockets... [Try " + str(tries) + "/5]")
            try:
                install('websockets')
                import site, imp
                imp.reload(site)
                print("Websockets installed.")
            except Exception as ex:
                print("An error occured when installing websockets: " + str(ex))
    from datetime import datetime
    print("[ChatServerUser] Done!")
    time.sleep(2)
    if __name__ == "__main__":
        global chatserveruser_halt
        while not chatserveruser_halt:
            try:
                async def mloop():
                    global chatserveruser_halt
                    connected = False
                    async with websockets.connect('ws://localhost:9009') as s:
                        while not chatserveruser_halt:
                            if not connected:

                                #EDIT
                                globals()["s"] = s
                                # connect to remote host
                                try :
                                    #EDIT
                                    async def setsend(msg):
                                        await s.send(msg)
                                    await setsend("cf7bcef89b9cf428535a77d5bdc972c8")
                                    await setsend("Server")
                                    await setsend("true")
                                    await setsend("206513b66a4eed9eb6b94e77cea1b23f")
                                    await setsend(platform.node())
                                    time.sleep(1)
                                    await setsend("~admin -System -" + administrators["system"])
                                    connected = True

                                except:
                                    pass
                            if connected:
                                if datetime.now().strftime("%H") == "23":
                                    if datetime.now().strftime("%M") == "59":
                                        #EDIT
                                        async def tasksend(msg):
                                            await s.send(msg)
                                        await tasksend("The Server will restart in 1 minute")
                                        time.sleep(60)
                                        await tasksend("~restart -" + administrators["system"])
                                        time.sleep(1)
                                        s.close()
                                        connected = False
                                        chatserveruser_halt = True
                asyncio.new_event_loop().run_until_complete(mloop())
            except Exception as ex:
                print('[ChatServerUser] There was an error: %s' % ex)
        #EDIT

        try:
            s.close()
        except:
            pass

class myThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print ("Starting " + self.name + " Thread")
        ChatServerUser()
        print ("Exiting " + self.name + " Thread")


try:
    if True:
       thread1 = myThread("ChatServerUser")
       thread1.start()
except Exception as ex:
    print("Error: unable to start server_chan thread")
    print("Error: " + str(ex))
    sys.exit()


import time, codecs
time.sleep(3)

print("Starting Logging...")
from datetime import datetime
filename = "logs\\" + datetime.now().strftime("log @ %Y-%m-%d %H-%M") + ".log"
try:
    log_file = codecs.open(filename, "w", "utf-8-sig")
    log_file.close()
except Exception as ex:
    print(str(ex))
    chatserveruser_halt = 1
    thread1.join()
    while True:
        pass

def Log(text):
    print(text)
    try:
        tolog = str(text) + "\r\n"
        file = codecs.open(filename, "a", "utf-8","utf-8-sig")
        file.write(tolog)
        file.close()
    except Exception as ex:
        print("Logging Error: " + str(ex))
        chatserveruser_halt = 1
        thread1.join()
        while True:
            pass

Log("Logging Successfully started!")
Log("Logging Started At: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
Log("Original Code By Samuel Simpson")
Log("Loading Chat Server...")


import sys, select, ast, os, hashlib, platform, asyncio
import pip

def install(package):
    pip.main(['install', '--user', package])
imported = False
tries = 0
while not imported:
    try:
        import socket, importlib
        globals()['websockets'] = importlib.import_module('websockets')

        imported = True
    except Exception as ex:
        print("An error occured when importing websockets: " + str(ex))
        tries += 1
        if tries == 6:
            print("Install Failed.")
            while True:
                pass
        print("Installing websockets... [Try " + str(tries) + "/5]")
        try:
            install('websockets')
            import site, imp
            imp.reload(site)
            print("Websockets installed.")
        except Exception as ex:
            print("An error occured when installing websockets: " + str(ex))

def timenow():
    return (str("[" + datetime.now().strftime('%H:%M:%S') + "] "))

HOST = "0.0.0.0"
SOCKET_LIST = set()
RECV_BUFFER = 4096
PORT = 9009
ips = []
admins = set()
usednicknames = []
globals()["restart"] = False
globals()["shutdown"] = False
TO_DELETE = set()



def toMD5(strtohash):
    MD5Hash = hashlib.md5(strtohash).hexdigest() #Convert to MD5 Here
    return(MD5Hash)

def loadid():
    message = timenow() + " Loading ID File..."
    Log(message)
    try:
        idfile = codecs.open("unique_ids.json", 'r', 'utf-8', 'utf-8-sig')
        globals()["id"] = ast.literal_eval(idfile.read())
        idfile.close()
        Log("Next ID: " + str(globals()["id"]))
        message = timenow() + " ID File Loaded"
        Log(message)
    except Exception as ex:
        message = timenow() + " An Error Occured: " + str(ex)
        Log(message)
        message = timenow() + " Creating empty ID file"
        Log(message)
        globals()["id"] = 0
        idfile = codecs.open("unique_ids.json", 'w', 'utf-8', 'utf-8-sig')
        idfile.write(str(globals()["id"]))
        idfile.close()

def newid():
    message = timenow() + " Creating new ID..."
    Log(message)
    idfile = codecs.open("unique_ids.json", 'w', 'utf-8','utf-8-sig')
    globals()["id"] += 1
    idfile.write(str(globals()["id"]))
    idfile.close()
    message = timenow() + " ID: " + str(id - 1)
    Log(message)
    message = timenow() + " ID Created."
    Log(message)
    return (toMD5(str(id - 1).encode()))

def loadbanlist():
    message = timenow() + " Loading Banlist..."
    Log(message)
    try:
        banlistfile = codecs.open("banned_users.json", 'r', 'utf-8', 'utf-8-sig')
        globals()["bannedusers"] = ast.literal_eval(banlistfile.read())
        banlistfile.close()
        Log("Banlist: " + str(globals()["bannedusers"]))
        message = timenow() + " Banlist Loaded"
        Log(message)
    except Exception as ex:
        message = timenow() + " An Error Occured: " + str(ex)
        Log(message)
        message = timenow() + " Creating empty banlist file"
        Log(message)
        globals()["bannedusers"] = []
        banlistfile = codecs.open("banned_users.json", 'w', 'utf-8', 'utf-8-sig')
        banlistfile.write(str(globals()["bannedusers"]))
        banlistfile.close()

def savebanlist():
    message = timenow() + " Saving banlist..."
    Log(message)
    banlistfile = codecs.open("banned_users.json", 'w', 'utf-8','utf-8-sig')
    banlistfile.write(str(globals()["bannedusers"]))
    banlistfile.close()
    message = timenow() + " Banlist saved"
    Log(message)

def loadadmins():
    message = timenow() + " Loading Admins..."
    Log(message)
    try:
        adminsfile = open("admins.json", 'r')
        globals()["administrators"] = ast.literal_eval(adminsfile.read())
        adminsfile.close()
        message = timenow() + " Admins Loaded"
        Log(message)
    except Exception as ex:
        message = timenow() + " An Error Occured: " + str(ex)
        Log(message)
        message = timenow() + " Creating empty admins file"
        Log(message)
        globals()["administrators"] = {
                                        "admin" : "25d55ad283aa400af464c76d713c07ad",
                                        "system" : "81dc9bdb52d04dc20036dbd8313ed055",
                                        }
        adminsfile = open("admins.json", 'w')
        adminsfile.write(str(globals()["administrators"]))
        adminsfile.close()

loadadmins()
loadbanlist()
loadid()

systempass = administrators["system"]

class Restart(Exception):
    pass
class Shutdown(Exception):
    pass

def chat_server():

    global fromip
    fromip = {}
    global sendnick
    sendnick = {}
    global ip
    ip = {}
    global nickname
    nickname = {}
    global username
    username = {}
    global host
    host = {}
    global fromname
    fromname = {}

    async def handleconn(sockfd, path):
        discon = False
        addr = sockfd.remote_address
        message = timenow() + " Connection from %s" % str(addr)
        Log(message)
        verif = (await sockfd.recv())
        #EDIT
        async def sockfdsend(msg):
            await sockfd.send(msg)
        if verif == "cf7bcef89b9cf428535a77d5bdc972c8":
            sockfdnickname = (await sockfd.recv())
            message = "Nickname: " + sockfdnickname
            Log(message)
            sockfdid = (await sockfd.recv())
            message = "HasID: " + sockfdid
            Log(message)
            if sockfdid.lower() == "false":
                idnew = newid()
                await sockfd.send(idnew.encode())
                time.sleep(0.5)
            sockfdusername = (await sockfd.recv())
            message = "Username: " + sockfdusername
            Log(message)
            sockfdhost = (await sockfd.recv())
            message = "Hostname: " + sockfdhost
            Log(message)
            if sockfdusername in globals()["bannedusers"]:
                message = timenow() + " [" + str(addr) + "] Sorry but you are banned from this chat server. Please ask the Server manager for assistance."
                await sockfdsend((message + "\n").encode())
                Log(message)
            else:
                if sockfdnickname in usednicknames or sockfdnickname == "server" and sockfdhost != hostname:
                    message = timenow() + " [Server] Sorry but the nickname you are trying to use is in use."
                    await sockfdsend((message + "\n").encode())
                    Log(message)
                else:
                    address = addr
                    sockfdip = address[0]
                    if sockfdip in ips:
                        message = timenow() + " [Server] Sorry but the ip you are trying to connect from is already connected."
                        await sockfdsend((message + "\n").encode())
                        Log(message)
                    else:
                        if  sockfdnickname == "" or len(sockfdnickname) > 31:
                            message = timenow() + " [Server] Sorry but your nickname is blank or too long, please create a nickname. If that doesn't work please contact a server administrator."
                            await sockfdsend((message + "\n").encode())
                            Log(message)
                        else:
                            dash = False
                            for i in sockfdnickname:
                                if i == "-":
                                    dash = True
                            if  dash:
                                message = timenow() + " [Server] Sorry but your nickname contains a hyphen (-), please create a nickname without one as that character is reserved."
                                await sockfdsend((message + "\n").encode())
                                Log(message)
                                message = timenow() + " [Server] If that doesn't work please contact a server administrator."
                                await sockfdsend((message + "\n").encode())
                                Log(message)
                            else:
                                if sockfdhost == "" or sockfdusername == "":
                                    message = timenow() + " [Server] Sorry but your hostname/username is reporting to be blank, please contact a server administrator."
                                    await sockfdsend((message + "\n").encode())
                                    Log(message)
                                else:
                                    ips.append(sockfdip)
                                    usednicknames.append(sockfdnickname)
                                    SOCKET_LIST.add(sockfd)
                                    fromip[sockfdip] = sockfd
                                    sendnick[str(sockfd)] = "[" + sockfdnickname + "]"
                                    ip[str(sockfd)] = sockfdip
                                    nickname[str(sockfd)] = sockfdnickname
                                    username[str(sockfd)] = sockfdusername
                                    host[str(sockfd)] = sockfdhost
                                    fromname[sockfdnickname] = sockfd
                                    message = timenow() + " Client (%s) connected" % nickname[str(sockfd)]
                                    Log(message)
                                    await broadcast(sockfd, (timenow() + nickname[str(sockfd)] + " entered the chat room"))
                                    while not (globals()["restart"] or globals()["shutdown"] or discon or sockfd in TO_DELETE):
                                            # process data recieved from client,
                                        #for sock in SOCKET_LIST:
                                        sock = sockfd
                                        if True:
                                            try:
                                                # receiving data from the socket.
                                                #EDIT
                                                if True:#sock != server_socket:
                                                    datain = await sock.recv()
                                                    #data = str(datain,'utf-8')
                                                    data = datain
                                                    nick = sendnick[str(sock)]
                                                    restart = False
                                                    shutdown = False

                                                    if data:
                                                        # there is something in the socket
                                                        if len(data) > 160:
                                                            try:
                                                                #EDIT
                                                                targetsock = sock
                                                                name = nickname[str(targetsock)]
                                                                message = timenow() + "[Server] You have sent a message that is too long and you are being kicked from the server."
                                                                def targetsocksend(msg):
                                                                    targetsock.send(msg)
                                                                targetsocksend((message + "\n").encode())
                                                                if targetsock in SOCKET_LIST:
                                                                    SOCKET_LIST.remove(targetsock)
                                                                if targetsock in admins:
                                                                    admins.remove(targetsock)
                                                                usednicknames.remove(name)
                                                                ips.remove(ip[str(targetsock)])
                                                                targetip = ip[str(targetsock)]
                                                                targetnick = nickname[str(targetsock)]
                                                                targetusername = username[str(targetsock)]
                                                                del fromip[targetip]
                                                                del sendnick[str(targetsock)]
                                                                del ip[str(targetsock)]
                                                                del nickname[str(targetsock)]
                                                                del username[str(targetsock)]
                                                                del host[str(targetsock)]
                                                                del fromname[targetnick]
                                                                time.sleep(2)

                                                                #EDIT
                                                                message = timenow() + "[Server] %s has been kicked from the server due to sending a message that is too long" % targetnick
                                                                await broadcast(sock, message)
                                                                Log(message)
                                                                discon = True
                                                            except Exception as ex:
                                                                message = timenow() + "[Server] An error occured: " + str(ex)
                                                                Log(message)
                                                        elif data[0] == "~":
                                                            message = timenow() + nick + ": " + data
                                                            Log(message)
                                                            #EDIT
                                                            async def send(message):
                                                                await sock.send((message + "\n").encode())
                                                                Log(message)
                                                            if data[:7] == "~admin " or data == "~admin":
                                                                data = data.split(' -', 2 )
                                                                try:
                                                                    user = data[1]
                                                                    user = str.lower(user)
                                                                    password = data[2]
                                                                    if user in administrators:
                                                                        if administrators.get(user) == password:
                                                                            admins.add(sock)
                                                                            message = timenow() + "[Server]" + nick + " has gained admin permissions"
                                                                            await broadcast(sock, message)
                                                                            Log(message)
                                                                        else:
                                                                            message = timenow() + "[Server] Incorrect Username or Password"
                                                                            await send(message)
                                                                    else:
                                                                        message = timenow() + "[Server] Incorrect Username or Password"
                                                                        await send(message)
                                                                except:
                                                                    message = timenow() + "[Server] Incorrect Syntax = ~admin -username -password"
                                                                    await send(message)
                                                            elif data[:6] == "~help " or data == "~help":
                                                                message = timenow() + ": Showing Help"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~admin -username -password = converts your session to an admin session"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~help = displays the help page"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~pm -targetnickname -message = sends a private message to a person with a certain nickname"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~users = displays a list of all users current connected"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~quit = disconnects you from the server"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~ping = returns your ping"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = ""
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "All of the following commands require admin permissions:"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~whois -targetnickname = tells you the username of the person with a certain nickname - ADMIN REQUIRED"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~kick -targetnickname = kicks a person with a certain ip from the server - ADMIN REQUIRED"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~ban -nickname = bans the username of the person using the nickname - ADMIN REQUIRED"
                                                                await send(message)
                                                                #time.sle`ep(0.05)
                                                                message = "~bannedusers = shows the list of banned usernames - ADMIN REQUIRED"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~unban -username = unbans the persons username - ADMIN REQUIRED"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~restart -restartpassword = restarts the server - ADMIN REQUIRED"
                                                                await send(message)
                                                                #time.sleep(0.05)
                                                                message = "~shutdown -shutdownpassword = shutdown the server - ADMIN REQUIRED"
                                                                await send(message)
                                                            elif data[:6] == "~ping " or data == "~ping":
                                                                message = timenow() + "[Server] Pong!"
                                                                await send(message)
                                                            elif data[:7] == "~whois " or data == "~whois":
                                                                if sock in admins:
                                                                    data = data.split(" -", 1)
                                                                    try:
                                                                        name = data[1]
                                                                        targetsock = fromname[name]
                                                                        targetip = ip[str(targetsock)]
                                                                        message = timenow() + "[Server] " + str(name) + " | " + str(host[str(targetsock)]) + " : " + str(username[str(targetsock)]) + " | " + str(targetip)
                                                                    except Exception as ex:
                                                                        print("whois error: " + str(ex))
                                                                        message = timenow() + "[Server] That person cannot be found"
                                                                    await send(message)
                                                                else:
                                                                    message = timenow() + "[Server] You do not have permission to do that"
                                                                    await send(message)
                                                            elif data[:6] == "~kick " or data == "~kick":
                                                                if sock in admins:
                                                                    try:
                                                                        data = data.split(" -", 1)
                                                                        name = data[1]
                                                                        if not name == "Server":
                                                                            try:
                                                                                #EDIT
                                                                                targetsock = fromname[name]
                                                                                async def targetsocksend(msg):
                                                                                    await targetsock.send(msg)
                                                                                message = timenow() + "[Server] You have been kicked from the server"
                                                                                await targetsocksend((message + "\n").encode())
                                                                                if targetsock in SOCKET_LIST:
                                                                                    SOCKET_LIST.remove(targetsock)
                                                                                if targetsock in admins:
                                                                                    admins.remove(targetsock)
                                                                                usednicknames.remove(name)
                                                                                ips.remove(ip[str(targetsock)])
                                                                                targetip = ip[str(targetsock)]
                                                                                targetnick = nickname[str(targetsock)]
                                                                                targetusername = username[str(targetsock)]
                                                                                del fromip[targetip]
                                                                                del sendnick[str(targetsock)]
                                                                                del ip[str(targetsock)]
                                                                                del nickname[str(targetsock)]
                                                                                del username[str(targetsock)]
                                                                                del host[str(targetsock)]
                                                                                del fromname[targetnick]
                                                                                #EDIT
                                                                                message = timenow() + "[Server] %s has been kicked from the server" % targetnick
                                                                                await broadcast(sock, message)
                                                                                Log(message)
                                                                                TO_DELETE.add(targetsock)
                                                                            except Exception as ex:
                                                                                message = timenow() + "[Server] That person cannot be found"
                                                                                await send(message)
                                                                        else:
                                                                            message = timenow() + "[Server] You do not have permission to do that"
                                                                            await send(message)
                                                                    except:
                                                                        message = timenow() + "[Server] Incorrect Syntax = ~kick -targetnickname"
                                                                        await send(message)
                                                                else:
                                                                    message = timenow() + "[Server] You do not have permission to do that"
                                                                    await send(message)
                                                            elif data[:13] == "~bannedusers " or data == "~bannedusers":
                                                                if sock in admins:
                                                                    message = timenow() + "[Server] Showing list of banned people:"
                                                                    await send(message)
                                                                    for user in globals()["bannedusers"]:
                                                                        await send(user)
                                                                else:
                                                                    message = timenow() + "[Server] You do not have permission to do that"
                                                                    await send(message)
                                                            elif data[:7] == "~unban " or data == "~unban":
                                                                try:
                                                                    data = data.split(" -",1)
                                                                    targetusername = data[1]
                                                                    if sock in admins:
                                                                        try:
                                                                            globals()["bannedusers"].remove(targetusername)
                                                                            savebanlist()
                                                                            message = timenow() + "[Server] Unbanned %s" % data[1]
                                                                            await send(message)
                                                                        except:
                                                                            message = timenow() + "[Server] Username not found"
                                                                            await send(message)
                                                                    else:
                                                                        message = timenow() + "[Server] You do not have permission to do that"
                                                                        await send(message)
                                                                except:
                                                                    message = timenow() + "[Server] Incorrect Syntax = ~unban -username"
                                                                    await send(message)
                                                            elif data[:4] == "~pm " or data == "~pm":
                                                                try:
                                                                    data = data.split(" -", 2)
                                                                    datatarget = data[1]
                                                                    datamessage = data[2]
                                                                    try:
                                                                        target = fromname[datatarget]
                                                                        async def targetsend(msg):
                                                                            await target.send(msg)
                                                                        message = timenow() + "[Private Message from " + nick + " to [" + datatarget + "]] " + datamessage
                                                                        await targetsend((message + "\n").encode())
                                                                        time.sleep(0.1)
                                                                    except:
                                                                        message = timenow() + "[Server] That person cannot be found"
                                                                except:
                                                                    message = timenow() + "[Server] Incorrect Syntax = ~pm -targetnickname -message"
                                                                await send(message)
                                                            elif data[:7] == "~users " or data == "~users":
                                                                message = timenow() + "[Server] Showing list of people currently connected:"
                                                                await send(message)
                                                                for user in usednicknames:
                                                                    await send("{" + user + "}")
                                                            elif data[:5] == "~ban " or data == "~ban":
                                                                data = data.split(" -", 1)
                                                                try:
                                                                    name = data[1]
                                                                    if sock in admins and not name == "Server":
                                                                        try:
                                                                            #EDIT
                                                                            targetsock = fromname[name]
                                                                            async def targetsocksend(msg):
                                                                                await targetsock.send(msg)
                                                                            message = timenow() + "[Server] You have been banned from the server"
                                                                            await targetsocksend((message + "\n").encode())
                                                                            if targetsock in SOCKET_LIST:
                                                                                SOCKET_LIST.remove(targetsock)
                                                                            if targetsock in admins:
                                                                                admins.remove(targetsock)
                                                                            usednicknames.remove(name)
                                                                            ips.remove(ip[str(targetsock)])
                                                                            targetip = ip[str(targetsock)]
                                                                            targetnick = nickname[str(targetsock)]
                                                                            targetusername = username[str(targetsock)]
                                                                            del fromip[targetip]
                                                                            del sendnick[str(targetsock)]
                                                                            del ip[str(targetsock)]
                                                                            del nickname[str(targetsock)]
                                                                            del username[str(targetsock)]
                                                                            del host[str(targetsock)]
                                                                            del fromname[targetnick]
                                                                            globals()["bannedusers"].append(targetusername)
                                                                            savebanlist()
                                                                            #EDIT
                                                                            message = timenow() + "[Server] %s has been banned from the server" % targetnick
                                                                            await broadcast(sock, message)
                                                                            Log(message)
                                                                            TO_DELETE.add(targetsock)
                                                                        except:
                                                                            message = timenow() + "[Server] That person cannot be found"
                                                                            await send(message)
                                                                    else:
                                                                        message = timenow() + "[Server] You do not have permission to do that"
                                                                        await send(message)
                                                                except:
                                                                    message = timenow() + "[Server] Incorrect Syntax = ~ban -nickname"
                                                                    await send(message)

                                                            elif data[:9] == "~restart " or data == "~restart":

                                                                data = data.split(" -", 1)
                                                                try:
                                                                    password = data[1]
                                                                    if sock in admins:
                                                                        if password == systempass:
                                                                            message = timenow() + "[Server] The Server Is Restarting, It will be back online within 5 minutes."
                                                                            await broadcast(sock, message)
                                                                            time.sleep(1)
                                                                            Log(message)
                                                                            restart = True
                                                                            globals()["restart"] = True
                                                                        else:
                                                                            message = timenow() + "[Server] Incorrect Password"
                                                                            await send(message)
                                                                    else:
                                                                        message = timenow() + "[Server] You do not have permission to do that"
                                                                        await send(message)
                                                                except:
                                                                    message = timenow() + "[Server] Incorrect Syntax = ~restart -restartpassword"
                                                                    await send(message)
                                                            elif data[:10] == "~shutdown " or data == "~shutdown":

                                                                data = data.split(" -", 1)
                                                                try:
                                                                    password = data[1]
                                                                    if sock in admins:
                                                                        if password == systempass:
                                                                            message = timenow() + "[Server] The Server Is Shutting Down, It will be back soon."
                                                                            await broadcast(sock, message)
                                                                            time.sleep(1)
                                                                            Log(message)
                                                                            shutdown = True
                                                                            globals()["shutdown"] = True
                                                                        else:
                                                                            message = timenow() + "[Server] Incorrect Password"
                                                                            await send(message)
                                                                    else:
                                                                        message = timenow() + "[Server] You do not have permission to do that"
                                                                        await send(message)
                                                                except:
                                                                    message = timenow() + "[Server] Incorrect Syntax = ~shutdown -shutdownpassword"
                                                                    await send(message)
                                                            elif data[:6] == "~quit " or data == "~quit":
                                                                try:
                                                                    name = nickname[str(sock)]
                                                                    #EDIT
                                                                    targetsock = fromname[name]
                                                                    async def targetsocksend(msg):
                                                                        await targetsock.send(msg)
                                                                    message = timenow() + "You have disconnected from the server"
                                                                    await targetsocksend((message + "\n").encode())
                                                                    if targetsock in SOCKET_LIST:
                                                                        SOCKET_LIST.remove(targetsock)
                                                                    if targetsock in admins:
                                                                        admins.remove(targetsock)
                                                                    usednicknames.remove(name)
                                                                    ips.remove(ip[str(targetsock)])
                                                                    targetip = ip[str(targetsock)]
                                                                    targetnick = nickname[str(targetsock)]
                                                                    targetusername = username[str(targetsock)]
                                                                    del fromip[targetip]
                                                                    del sendnick[str(targetsock)]
                                                                    del ip[str(targetsock)]
                                                                    del nickname[str(targetsock)]
                                                                    del username[str(targetsock)]
                                                                    del host[str(targetsock)]
                                                                    del fromname[targetnick]
                                                                    #EDIT
                                                                    message = timenow() + "[Server] %s has disconnected from the server" % targetnick
                                                                    await broadcast(sock, message)
                                                                    Log(message)
                                                                    discon = True
                                                                except Exception as ex:
                                                                    message = timenow() + "[Server] An Error Occured: " + str(ex)
                                                                    Log(message)


                                                            else:
                                                                message = timenow() + "[Server] Unknown Command, type ~help to see commands"
                                                                await send(message)
                                                        else:
                                                            message = timenow() + nick + ": " + data
                                                            await broadcast(sock, message)
                                                            Log(message)
                                                    else:
                                                        # remove the socket that's broken
                                                        name = nickname[str(sock)]
                                                        if sock in SOCKET_LIST:
                                                            SOCKET_LIST.remove(sock)
                                                        if sock in admins:
                                                            admins.remove(sock)
                                                        usednicknames.remove(name)
                                                        ips.remove(ip[str(sock)])
                                                        targetip = ip[str(sock)]
                                                        targetnick = nickname[str(sock)]
                                                        targetusername = username[str(sock)]
                                                        del fromip[targetip]
                                                        del sendnick[str(sock)]
                                                        del ip[str(sock)]
                                                        del nickname[str(sock)]
                                                        del username[str(sock)]
                                                        del host[str(sock)]
                                                        del fromname[targetnick]
                                                        message = timenow() + " Client (%s) is offline" % targetnick
                                                        await broadcast(sock, message)
                                                        Log(message)
                                                        discon = True
                                            # exception
                                            except Exception as ex:
                                                Log(timenow() + str(ex))
                                                Log(timenow() + "Removing Broken Connection...")
                                                try:
                                                    name = nickname[str(sock)]
                                                    #print(str(name))
                                                    if sock in SOCKET_LIST:
                                                        SOCKET_LIST.remove(sock)
                                                    if sock in admins:
                                                        admins.remove(sock)
                                                    usednicknames.remove(name)
                                                    ips.remove(ip[str(sock)])
                                                    targetip = ip[str(sock)]
                                                    targetnick = nickname[str(sock)]
                                                    targetusername = username[str(sock)]
                                                    del fromip[targetip]
                                                    del sendnick[str(sock)]
                                                    del ip[str(sock)]
                                                    del nickname[str(sock)]
                                                    del username[str(sock)]
                                                    del host[str(sock)]
                                                    del fromname[targetnick]
                                                    message = timenow() + " Client (%s) is offline" % targetnick
                                                    await broadcast(sock, message)
                                                    Log(message)
                                                except Exception as ex:
                                                    Log(str(ex))
                                                    continue
                                                discon = True
                                                continue
                                    try:
                                        TO_DELETE.remove(sock)
                                    except:
                                        pass

        else:
            message = timenow() + " [Server] Sorry but the verification code was invalid. Please contact a server administrator."
            await sockfdsend((message + "\n").encode())
            Log(message)

    #EDIT

    # add server socket object to the list of readable connections
    start_server = websockets.serve(handleconn, host=HOST, port=PORT)

    #SOCKET_LIST.append(server_socket)

    #EDIT
    hostname = platform.node() # Get local machine name
    message = timenow() + " Server Hostname: " + hostname
    Log(message)
    message = timenow() + " Chat server started on port " + str(PORT)
    Log(message)
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(start_server)
            if globals()["restart"]:
                raise Restart
            if globals()["shutdown"]:
                raise Shutdown
        except Restart:
            raise Restart
        except Shutdown:
            raise Shutdown
    #asyncio.get_event_loop().run_forever()

    #EDIT
    #server_socket.close()

# broadcast chat messages to all connected clients
async def broadcast (sock, message):
    message = message + "\n"
    for socket in SOCKET_LIST:
        # send the message only to peer
        if True:#socket != server_socket:# and socket != sock :
            try:
                #EDIT
                await socket.send(message.encode())
            except Exception as ex:
                print("Broadcast Error: " + str(ex))
                # broken socket connection
                #socket.close()
                # broken socket, remove it
                try:
                    name = nickname[str(sock)]
                    if sock in SOCKET_LIST:
                        SOCKET_LIST.remove(sock)
                    if sock in admins:
                        admins.remove(sock)
                    usednicknames.remove(name)
                    ips.remove(ip[str(sock)])
                    targetip = ip[str(sock)]
                    targetnick = nickname[str(sock)]
                    targetusername = username[str(sock)]
                    del fromip[targetip]
                    del sendnick[str(sock)]
                    del ip[str(sock)]
                    del nickname[str(sock)]
                    del username[str(sock)]
                    del host[str(sock)]
                    del fromname[targetnick]
                    message = timenow() + " Client (%s) is offline" % targetnick
                    await broadcast(sock, message)
                    Log(message)
                except Exception as ex:
                    Log(str(ex))
                    continue

excode = 0

if __name__ == "__main__":
    Log("Done!")
    try:
        chat_server()
        excode = 0
    except Restart:
        message = timenow() + "===RESTARTING==="
        Log(message)
        time.sleep(2)
        excode = 2
        #os.system("sudo shutdown -r now")
    except Shutdown:
        message = timenow() + "===SHUTTING_DOWN==="
        Log(message)
        excode = 1
        #os.system("sudo shutdown -h now")
    except Exception as ex:
        message = timenow() + " An error occured: " + str(ex)
        Log(message)
        time.sleep(2)
        excode = 2
        #os.system("sudo shutdown -r now")


os._exit(excode)
