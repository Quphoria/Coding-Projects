# filename = input("Target File: ")
filename = "littleschoolbus.bmp"

file = open(filename,"rb")
filedata = file.read()

# print(get_lsbs_str(filedata))
binary = ""
for fpos in range(len(filedata)):
    #print(chr(filedata[fpos]))
    charbin = "{0:b}".format(filedata[fpos])
    binary += charbin[len(charbin)-1]
# print(binary)

output = ""
shift = 7
bpos = shift
while bpos + 7 < shift+512:
    output += chr(int(binary[bpos:bpos+7],2))
    bpos += 8
print(output)
