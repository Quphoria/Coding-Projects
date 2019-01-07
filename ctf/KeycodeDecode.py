keyfilename = "keyboardscancodes.txt"
keyfile = open(keyfilename)
keylist = keyfile.readlines()
keylists = []
for klist in keylist:
    keylists.append(klist.replace("\n","").split(":"))
keydict = {}
for keyl in keylists:
    if len(keyl) > 2:
        dval = {keyl[0]:keyl[1], keyl[0] + "U":keyl[2]}
    else:
        dval = {keyl[0]:keyl[1], keyl[0] + "U":keyl[1]}
    keydict.update(dval)
# keydict.update({"20":"LeftShift","20U":"LeftShift"})
# print(keydict)

global Capslock
Capslock = False
global altkey
altkey = False
def decode(packet):
    global Capslock
    global altkey
    altkey = False
    if len(packet) > 0:
        packetdata = ""
        for cpos in range(len(packet)):
            pv = packet[cpos].upper()
            if pv != "" and pv != "00":
                if altkey:
                    pfunction = keydict[pv + "U"]
                else:
                    pfunction = keydict[pv]
                # print(pfunction)
                if pfunction == "LeftShift" or pfunction == "RightShift" or (cpos == 0 and packet[cpos] == "20"):
                    altkey = True
                elif pfunction == "Caps Lock":
                    Capslock = not Capslock
                else:
                    packetdata += pfunction
        print(packetdata)
        return packetdata
    else:
        return ""
