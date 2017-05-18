# chat_client.py


class ChatWindow:
    import platform, os, time, hashlib
    from datetime import datetime
    from itertools import chain

    def timenow():
        return ("[" + datetime.now().strftime('%H:%M:%S') + "]")

    def toMD5(strtohash):
        MD5Hash = hashlib.md5(strtohash).hexdigest() #Convert to MD5 Here
        return(MD5Hash)
    def longcallback():
        print("CB")
        msg = document.getElementById ('text_1') .innerHTML
        c = msg[0:150]
        outtext = ""
        for letter in c:
            if letter != "\\":
                outtext = outtext + letter
        document.getElementById ('text_1') .innerHTML = outtext
    def smallcallback(msg):
        c = msg.get()[0:30]
        outtext = ""
        for letter in c:
            if letter != "\\":
                outtext = outtext + letter
        msg.set(outtext)
    def messagein(mgdt):
        Log(mgdt.decode())
    def Log(msg):
        msg = msg.replace("\n","<br>")
        document.getElementById ('frag_1') .innerHTML = document.getElementById ('frag_1') .innerHTML + msg
    def sendmsg(dts):
        print("sending " + str(dts))
        dtp = dts
    def sendnewmessage():
        globals()["msgdata"] = document.getElementById ('text_1') .innerHTML
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
        sendmsg(msgdata.encode())
        document.getElementById ('text_1') .innerHTML = ""

    def __init__(self):

        try:

            open = False
            firsttime = True

            connected = False
            globals()["disconnected"] = False
            while not globals()["disconnected"]:

                if not connected:

                    hostserv = "ws://PCOWNER:9009/"

                    # connect to remote host
                    try:

                        print("connect with " + str(hostserv))
                        sendmsg("cf7bcef89b9cf428535a77d5bdc972c8".encode())
                        time.sleep(0.5)
                        sendmsg("test1".encode())
                        time.sleep(0.5)
                        sendmsg((os.getlogin()).encode())
                        time.sleep(0.5)
                        sendmsg(platform.node().encode())
                        message = 'Connected to remote host. You can start sending messages.'
                        message = message + "\n"
                        Log(message)
                        message = 'Type ~help to view commands.'
                        message = message + "\n"
                        Log(message)
                        connected = True
                    except Exception as ex:
                        Log("Unable to connect.\n")
                        print("A Connection Error Occured: " + str(ex))
        except Exception as ex:
            print("Error: " + str(ex))
