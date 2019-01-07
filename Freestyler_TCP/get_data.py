import socket
host = "127.0.0.1"
port = 3332
while True:
    fs_code = input("Request Code: ")
    if fs_code:
        if int(fs_code) > 0 and int(fs_code) < 255 and ("0" + str(int(fs_code)) == fs_code or "00" + str(int(fs_code)) == fs_code):
            request = "FSBC" + fs_code + chr(0) + chr(0) + chr(1)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,port))
            s.settimeout(1)
            s.send(request.encode())
            data = s.recv(4096)
            print(data)
            s.close()
        else:
            print("Invalid Code.")
