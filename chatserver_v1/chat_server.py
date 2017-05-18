# chat_server.py
import time
time.sleep(3)

print("Starting Logging...")
from datetime import datetime
filename = "logs\\" + datetime.now().strftime("log @ %Y-%m-%d %H-%M") + ".log"
log_file = open(filename, "w")
log_file.close()

def Log(text):
    file = open(filename, "a")
    file.write(str(text) + "\n")
    file.close()
    print(text)


Log("Logging Successfully started!")
Log("Logging Started At: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
Log("Original Code By Samuel Simpson")
Log("Loading Chat Server...")

import sys, socket, select, ast

def timenow():
    return (str("[" + datetime.now().strftime('%H:%M:%S') + "]"))

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9009
ips = []
admins = []
usednicknames = []

def loadbanlist():
    message = timenow() + " Loading Banlist..."
    Log(message)
    try:
        banlistfile = open("banned_users.json", 'r')
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
        banlistfile = open("banned_users.json", 'w')
        banlistfile.write(str(globals()["bannedusers"]))
        banlistfile.close()

def savebanlist():
    message = timenow() + " Saving banlist..."
    Log(message)
    banlistfile = open("banned_users.json", 'w')
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
                                        "admin" : "12345678",
                                        "system" : "1234",
                                        }
        adminsfile = open("admins.json", 'w')
        adminsfile.write(str(globals()["administrators"]))
        adminsfile.close()

loadadmins()
loadbanlist()

systempass = "1234"

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

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)

    hostname = socket.gethostname() # Get local machine name
    message = timenow() + " Server Hostname: " + hostname
    Log(message)
    message = timenow() + " Chat server started on port " + str(PORT)
    Log(message)

    while True:
        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        time.sleep(0.1)
        for sock in ready_to_read:
            # a new connection request recieved
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                message = timenow() + " Connection from %s" % str(addr)
                Log(message)
                sockfdnickname = sockfd.recv(RECV_BUFFER)
                message = "Nickname: " + sockfdnickname.decode()
                Log(message)
                sockfdusername = sockfd.recv(RECV_BUFFER)
                message = "Username: " + sockfdusername.decode()
                Log(message)
                sockfdhost = sockfd.recv(RECV_BUFFER)
                message = "Hostname: " + sockfdhost.decode()
                Log(message)
                if sockfdusername.decode() in globals()["bannedusers"]:
                    message = timenow() + " [" + str(addr) + "] Sorry but you are banned from this chat server. Please ask the Server manager for assistance."
                    sockfd.send(message.encode())
                    Log(message)
                else:
                    if sockfdnickname.decode() in usednicknames or sockfdnickname.lower() == "server" and sockfdhost != hostname:
                        message = timenow() + " [Server] Sorry but the nickname you are trying to use is in use."
                        sockfd.send(message.encode())
                        Log(message)
                    else:
                        address = str(addr).split("'", 2)
                        sockfdip = address[1]
                        if sockfdip in ips:
                            message = timenow() + " [Server] Sorry but the ip you are trying to connect from is already connected."
                            sockfd.send(message.encode())
                            Log(message)
                        else:
                            ips.append(sockfdip)
                            usednicknames.append(sockfdnickname.decode())
                            SOCKET_LIST.append(sockfd)
                            fromip[sockfdip] = sockfd
                            sendnick[str(sockfd)] = "[" + sockfdnickname.decode() + "]"
                            ip[str(sockfd)] = sockfdip
                            nickname[str(sockfd)] = sockfdnickname.decode()
                            username[str(sockfd)] = sockfdusername.decode()
                            host[str(sockfd)] = sockfdhost.decode()
                            fromname[sockfdnickname.decode()] = sockfd
                            message = timenow() + " Client (%s) connected" % nickname[str(sockfd)]
                            Log(message)
                            broadcast(server_socket, sockfd, (timenow() + nickname[str(sockfd)] + " entered our chatting room"))

            # a message from a client, not a new connection
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = str(sock.recv(RECV_BUFFER).decode())
                    nick = sendnick[str(sock)]
                    restart = False
                    shutdown = False
                    if data:
                        # there is something in the socket
                        if data[0] == "~":
                            message = timenow() + nick + ": " + data
                            Log(message)
                            def send(message):
                                sock.send(message.encode())
                                Log(message)
                            if data[:6] == "~admin":
                                data = data.split(' -', 2 )
                                try:
                                    user = data[1]
                                    user = str.lower(user)
                                    password = data[2]
                                    if user in administrators:
                                        if administrators.get(user) == password:
                                            admins.append(sock)
                                            message = timenow() + "[Server]" + nick + " has gained admin permissions"
                                            broadcast(server_socket, sock, message)
                                            Log(message)
                                        else:
                                            message = timenow() + "[Server] Incorrect Username or Password"
                                            send(message)
                                    else:
                                        message = timenow() + "[Server] Incorrect Username or Password"
                                        send(message)
                                except:
                                    message = timenow() + "[Server] Incorrect Syntax = ~admin -username -password"
                                    send(message)
                            elif data[:5] == "~help":
                                message = timenow() + ": Showing Help"
                                send(message)
                                time.sleep(0.2)
                                message = "~admin -username -password = converts your session to an admin session"
                                send(message)
                                time.sleep(0.2)
                                message = "~help = displays the help page"
                                send(message)
                                time.sleep(0.2)
                                message = "~pm -targetnickname -message = sends a private message to a person with a certain nickname"
                                send(message)
                                time.sleep(0.2)
                                message = "~users = displays a list of all users current connected"
                                send(message)
                                time.sleep(0.2)
                                message = "~quit = disconnects you from the server"
                                send(message)
                                time.sleep(0.2)
                                message = "~ping = returns the speed of your connection to the server"
                                send(message)
                                time.sleep(0.2)
                                message = "All of the following commands require admin permissions:"
                                send(message)
                                time.sleep(0.2)
                                message = "~whois -targetnickname = tells you the username of the person with a certain nickname - ADMIN REQUIRED"
                                send(message)
                                time.sleep(0.2)
                                message = "~kick -targetnickname = kicks a person with a certain ip from the server - ADMIN REQUIRED"
                                send(message)
                                time.sleep(0.2)
                                message = "~ban -nickname = bans the username of the person using the nickname - ADMIN REQUIRED"
                                send(message)
                                time.sleep(0.2)
                                message = "~bannedusers = shows the list of banned usernames - ADMIN REQUIRED"
                                send(message)
                                time.sleep(0.2)
                                message = "~unban -username = ubans the persons username - ADMIN REQUIRED"
                                send(message)
                                time.sleep(0.2)
                                message = "~restart -restartpassword = restarts the server - ADMIN REQUIRED"
                                send(message)
                                time.sleep(0.2)
                                message = "~shutdown -shutdownpassword = shutdown the server - ADMIN REQUIRED"
                                send(message)
                            elif data[:5] == "~ping":
                                message = timenow() + "[Server] Pong!"
                                send(message)
                            elif data[:6] == "~whois":
                                if sock in admins:
                                    data = data.split(" -", 1)
                                    try:
                                        name = data[1]
                                        targetsock = fromname[name]
                                        message = timenow() + "[Server] " + name + " | " + host[str(targetsock)] + " : " + username[str(targetsock)]
                                    except:
                                        message = timenow() + "[Server] That person cannot be found"
                                    send(message)
                                else:
                                    message = timenow() + "[Server] You do not have permission to do that"
                                    send(message)
                            elif data[:5] == "~kick":
                                if sock in admins:
                                    try:
                                        data = data.split(" -", 1)
                                        name = data[1]
                                        if not name == "Server":
                                            try:
                                                targetsock = fromname[name]
                                                message = timenow() + "[Server] You have been kicked from the server"
                                                targetsock.send(message.encode())
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
                                                targetsock.close()
                                                message = timenow() + "[Server] %s has been kicked from the server" % targetnick
                                                broadcast(server_socket, sock, message)
                                                Log(message)
                                            except Exception as ex:
                                                message = timenow() + "[Server] That person cannot be found"
                                                send(message)
                                        else:
                                            message = timenow() + "[Server] You do not have permission to do that"
                                            send(message)
                                    except:
                                        message = timenow() + "[Server] Incorrect Syntax = ~kick -targetnickname"
                                        send(message)
                                else:
                                    message = timenow() + "[Server] You do not have permission to do that"
                                    send(message)
                            elif data[:12] == "~bannedusers":
                                if sock in admins:
                                    message = timenow() + "[Server] Showing list of banned people:"
                                    send(message)
                                    for user in globals()["bannedusers"]:
                                        send(user)
                                else:
                                    message = timenow() + "[Server] You do not have permission to do that"
                                    send(message)
                            elif data[:6] == "~unban":
                                try:
                                    data = data.split(" -",1)
                                    targetusername = data[1]
                                    if sock in admins:
                                        try:
                                            globals()["bannedusers"].remove(targetusername)
                                            savebanlist()
                                            message = timenow() + "[Server] Unbanned %s" % data[1]
                                            send(message)
                                        except:
                                            message = timenow() + "[Server] Username not found"
                                            send(message)
                                    else:
                                        message = timenow() + "[Server] You do not have permission to do that"
                                        send(message)
                                except:
                                    message = timenow() + "[Server] Incorrect Syntax = ~unban -username"
                                    send(message)
                            elif data[:3] == "~pm":
                                try:
                                    data = data.split(" -", 2)
                                    datatarget = data[1]
                                    datamessage = data[2]
                                    try:
                                        target = fromname[datatarget]
                                        message = timenow() + "[Private Message from " + nick + " to " + datatarget + "] " + datamessage
                                        target.send(message.encode())
                                        time.sleep(0.1)
                                    except:
                                        message = timenow() + "[Server] That person cannot be found"
                                except:
                                    message = timenow() + "[Server] Incorrect Syntax = ~pm -targetnickname -message"
                                send(message)
                            elif data[:6] == "~users":
                                message = timenow() + "[Server] Showing list of people currently connected:"
                                send(message)
                                for user in usednicknames:
                                    send(user)
                            elif data[:4] == "~ban":
                                data = data.split(" -", 1)
                                try:
                                    name = data[1]
                                    if sock in admins and not name == "Server":
                                        try:
                                            targetsock = fromname[name]
                                            message = timenow() + "[Server] You have been banned from the server"
                                            targetsock.send(message.encode())
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
                                            targetsock.close()
                                            message = timenow() + "[Server] %s has been banned from the server" % nick
                                            broadcast(server_socket, sock, message)
                                            Log(message)
                                        except:
                                            message = timenow() + "[Server] That person cannot be found"
                                            send(message)
                                    else:
                                        message = timenow() + "[Server] You do not have permission to do that"
                                        send(message)
                                except:
                                    message = timenow() + "[Server] Incorrect Syntax = ~ban -nickname"
                                    send(message)

                            elif data[:8] == "~restart":

                                data = data.split(" -", 1)
                                try:
                                    password = data[1]
                                    if sock in admins:
                                        if password == systempass:
                                            message = timenow() + "[Server] The Server Is Restarting, It will be back online within 5 minutes."
                                            broadcast(server_socket, sock, message)
                                            time.sleep(1)
                                            Log(message)
                                            restart = True
                                        else:
                                            message = timenow() + "[Server] Incorrect Password"
                                            send(message)
                                    else:
                                        message = timenow() + "[Server] You do not have permission to do that"
                                        send(message)
                                except:
                                    message = timenow() + "[Server] Incorrect Syntax = ~restart -restartpassword"
                                    send(message)
                            elif data[:8] == "~shutdown":

                                data = data.split(" -", 1)
                                try:
                                    password = data[1]
                                    if sock in admins:
                                        if password == systempass:
                                            message = timenow() + "[Server] The Server Is Shutting Down, It will be back soon."
                                            broadcast(server_socket, sock, message)
                                            time.sleep(1)
                                            Log(message)
                                            shutdown = True
                                        else:
                                            message = timenow() + "[Server] Incorrect Password"
                                            send(message)
                                    else:
                                        message = timenow() + "[Server] You do not have permission to do that"
                                        send(message)
                                except:
                                    message = timenow() + "[Server] Incorrect Syntax = ~shutdown -shutdownpassword"
                                    send(message)
                            elif data[:5] == "~quit":
                                try:
                                    name = nickname[str(sock)]
                                    targetsock = fromname[name]
                                    message = timenow() + "You have disconnected from the server"
                                    targetsock.send(message.encode())
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
                                    targetsock.close()
                                    message = timenow() + "[Server] %s has disconnected from the server" % targetnick
                                    broadcast(server_socket, sock, message)
                                    Log(message)
                                except Exception as ex:
                                    message = timenow() + "[Server] An Error Occured: " + str(ex)
                                    Log(message)


                            else:
                                message = timenow() + "[Server] Unknown Command, type ~help to see commands"
                                send(message)
                        else:
                            message = timenow() + nick + ": " + data
                            broadcast(server_socket, sock, message)
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
                        broadcast(server_socket, sock, message)
                        Log(message)
                # exception
                except Exception as ex:
                    Log(str(ex))
                    continue
                if restart:
                    raise Restart()
                if shutdown:
                    raise Shutdown()

    server_socket.close()

# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket:# and socket != sock :
            try:
                socket.send(message.encode())
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)



if __name__ == "__main__":
    Log("Done!")
    try:
        chat_server()
        input()
    except Restart:
        message = timenow() + "===RESTARTING==="
        Log(message)
        os.system("sudo shutdown -r now")
    except Shutdown:
        message = timenow() + "===SHUTTING_DOWN==="
        Log(message)
        os.system("sudo shutdown -h now")
    except Exception as ex:
        message = timenow() + " An error occured: " + str(ex)
        Log(message)
        os.system("sudo shutdown -r now")
