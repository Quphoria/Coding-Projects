import socket, time, select, sys, select
from datetime import datetime
HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 911
ID = 0
SOCKETS = {}
IDS = {}
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)
server_socket.settimeout(2)
SOCKET_LIST.append(server_socket)
SOCKETS.update({server_socket:[ID,"127.0.0.1"]})
ID = ID + 1
print("Server Successfully Started")
def Log(text):
    print(text)

def timenow():
    return (str("[" + datetime.now().strftime('%H:%M:%S') + "]"))

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def checkforconnections():
    x = 0
    while x < 15:
            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
            time.sleep(0.1)
            for sock in ready_to_read:
                try:
                    # a new connection request recieved
                    if sock == server_socket:
                        sockfd, addr = server_socket.accept()
                        message = timenow() + " Connection from %s" % str(addr)
                        Log(message)
                        sockfd.send(str(ID).encode())
                        hostname = sockfd.recv(4096).decode()
                        SOCKET_LIST.append(sockfd)
                        SOCKETS.update({sockfd:[ID,addr,hostname]})
                        IDS.update({ID:sockfd})
                        globals()["ID"] = globals()["ID"] + 1
                        x = x - 1
                except Exception as ex:
                    print(str(ex))
                # a message from a client, not a new connection
                else:
                    pass
            x = x + 1

def broadcast (message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket:
            try:
                socket.send(message.encode())
                if message == "isconnectionactive":
                    time.sleep(0.2)
                    socket.recv(4096)
            except Exception as ex:
                print(str(ex))
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    sockid = globals()["SOCKETS"][socket][0]
                    SOCKET_LIST.remove(socket)
                    globals()["SOCKETS"] = removekey(globals()["SOCKETS"],socket)
                    globals()["IDS"] = removekey(globals()["IDS"],sockid)

while True:
    print("Command: ")
    data = input()
    if data.lower() == "connection" or data.lower() == "connections":
        broadcast("isconnectionactive")
        checkforconnections()
        print("TOTAL CONNECTIONS: " + str(len(SOCKET_LIST) - 1))
    elif data.lower() == "quit":
        while (len(SOCKET_LIST) - 1) > 0:
            broadcast("exit")
            time.sleep(0.5)
        sys.exit()
    elif data.lower() == "shutdown":
        while (len(SOCKET_LIST) - 1) > 0:
            broadcast("shutdown")
            time.sleep(0.5)
        sys.exit()
    elif data.lower() == "exit":
        while (len(SOCKET_LIST) - 1) > 0:
            broadcast("exit")
            time.sleep(0.5)
    elif data.lower() == "clients":
        print("Syntax: [ID, \"ADDRESS\"]")
        for i in SOCKETS:
            if SOCKETS[i][0] != 0:
                print(str(SOCKETS[i]))
    elif data.lower() == "recieve":
        try:
            ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],3)
            print(len(ready_to_read))
            print("to")
            for sock in ready_to_read:
                print("Read")
                print(sock)
                data = sock.recv(RECV_BUFFER)
                if data:
                    print(str(data))
        except Exception as ex:
            pass
    elif data.lower()[:4] == "send":
        try:
            data = data.split(" -",2)
            targetidinput = data[1]
            targets = []
            try:
                targets.append(int(targetidinput))
            except:
                try:
                    targetidinput = targetidinput.split(",")
                    for targetselection in targetidinput:
                        try:
                            targets.append(int(targetselection))
                        except:
                            try:
                                targetselectionrange = targetselection.split("-")
                                for rangeid in range(int(targetselectionrange[0]),int(targetselectionrange[1]) + 1):
                                    targets.append(int(rangeid))
                            except:
                                pass
                except:
                    pass
            for targetid in targets:
                if targetid in globals()["IDS"] and targetid != 0:
                    socket = globals()["IDS"][targetid]
                    message = data[2]
                    try:
                        socket.send(message.encode())
                    except Exception as ex:
                        print(str(ex))
                        # broken socket connection
                        socket.close()
                        # broken socket, remove it
                        if socket in SOCKET_LIST:
                            sockid = globals()["SOCKETS"][socket][0]
                            SOCKET_LIST.remove(socket)
                            globals()["SOCKETS"] = removekey(globals()["SOCKETS"],socket)
                            globals()["IDS"] = removekey(globals()["IDS"],sockid)
                else:
                    print("Client ID " + str(targetid) + " not found.")
        except Exception as ex:
            print(str(ex))
            print("Incorrect Syntax. Syntax:  send -ID -Command")

    else:
        broadcast(data)
    time.sleep(0.1)
    broadcast("isconnectionactive")
