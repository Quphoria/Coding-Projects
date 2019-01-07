import KeycodeDecode

filename = "usbdata.txt"
file = open(filename)
usbdata = []
lines = file.readlines()
# print(lines)

for line in lines:
    # print(line)
    data = ""
    line = line.replace(" ","")
    # print(line)
    line = line.replace("\x00","")
    # print(line)
    line = line.replace("\n","")
    # print(line)
    datalist = line.split(":")
    datalist = datalist[:3]
    outdatalist = []
    # print(datalist)
    for val in datalist:
        if val != "":
            outdatalist.append(val)
    if outdatalist != []:
        print(outdatalist)
        usbdata.append(outdatalist)
# print(usbdata)
output = ""
for line in usbdata:
    if line != ["00","00","00"]:
        print(line)
        output += KeycodeDecode.decode(line)
print(output)
