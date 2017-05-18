# chatserveruser.py
print("[ChatServerUser] Loading...")
import sys, socket, select, os, time
from datetime import datetime
connected = False
print("[ChatServerUser] Done!")


if __name__ == "__main__":
    while True:
        try:
            while True:

                if not connected:

                    host = "localhost"
                    port = 9009

                    globals()["s"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.2)

                    # connect to remote host
                    try :
                        s.connect((host, port))
                        s.send("Server".encode())
                        time.sleep(0.5)
                        s.send("pi".encode())
                        time.sleep(0.5)
                        s.send(socket.gethostname().encode())
                        time.sleep(3)
                        s.send("~admin -System -1234".encode())
                        connected = True

                    except :
                        pass
                if connected:
                    if datetime.now().strftime("%H") == "23":
                        if datetime.now().strftime("%M") == "59":
                            s.send("The Server will restart in 1 minute".encode())
                            time.sleep(60)
                            s.send("~restart -1234".encode())
                            time.sleep(60)
                            s.close()
                            s.destroy()
                            connected = False
        except Exception as ex:
            print('[ChatServerUser] There was an error: %s' % ex)
    s.close()
    s.destroy()
