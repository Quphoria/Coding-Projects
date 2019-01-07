import socket
host = "127.0.0.1"
port = 3332
while True:
    fs_code = input("Request Code: ")
    a_code = input("Argument: ")
    o_code = input("Optional: ")
    if fs_code and a_code and o_code:
        if int(fs_code) >= 0 and int(fs_code) <= 999 and (str(int(fs_code)) == fs_code or "0" + str(int(fs_code)) == fs_code or "00" + str(int(fs_code)) == fs_code):
            if int(a_code) >= 0 or int(a_code) <= 255 and (str(int(a_code)) == a_code or "0" + str(int(a_code)) == a_code or "00" + str(int(a_code)) == a_code):
                if int(o_code) >= 0 and int(o_code) <= 999 and (str(int(o_code)) == o_code or "0" + str(int(o_code)) == o_code or "00" + str(int(o_code)) == o_code):
                    request = "FSOC" + fs_code + a_code + o_code
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((host,port))
                    s.settimeout(1)
                    s.send(request.encode())
                    # data = s.recv(4096)
                    # print(data)
                    s.close()
                else:
                    print("Invalid Optional.")
            else:
                print("Invalid Argument.")
        else:
            print("Invalid Code.")
