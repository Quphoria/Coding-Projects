import random, time
startcode = 65
fromalphabet = {}
toalphabet = {}
for i in range(startcode,startcode+26):
    fromalphabet.update({chr(i):i-startcode})
    toalphabet.update({i-startcode:chr(i)})

x = []
y = []

gotrange = False
while not gotrange:
    try:
        print("Please Enter a valid letter range, i.e: A-F")
        lrangeinput = input("Range: ")[:3]
        lrangein = str(lrangeinput).split('-')
        if len(lrangein) == 2:
            lrange = range(fromalphabet[str(lrangein[0]).capitalize()],fromalphabet[str(lrangein[1]).capitalize()]+1)
            if lrange[0] <= lrange[1]:
                for i in lrange:
                    x.append(toalphabet[i])
                gotrange = True
        print()
    except:
        pass

gotrange = False
while not gotrange:
    try:
        print("Please Enter a valid number range, i.e: 1-10")
        nrangeinput = input("Range: ")
        nrangein = str(nrangeinput).split('-',1)
        if len(nrangein) == 2:
            nrange = range(int(nrangein[0]),int(nrangein[1])+1)
            if nrange[0] <= nrange[1]:
                for i in nrange:
                    y.append(i)
                gotrange = True
        print()
    except:
        pass

gotmode = False
while not gotmode:
    try:
        mode = input("Do you want to allow coordinates to repeat? [Y/N]: ")[:1].lower()
        if mode == "y" or mode == "n":
            gotmode = True
        print()
    except:
        pass

print("Press Enter for next coordinate")

xy = []
xy2 = []
for i in x:
    for j in y:
        xy.append(str(i)+str(j))
        xy2.append(str(i)+str(j))
continuelist = True
while continuelist:
    if len(xy) > 0:
        idl = random.randint(0,len(xy)-1)
        print()
        value = xy[idl]
        if mode == "n":
            del xy[idl]
        input(str(value))
        time.sleep(1)
    else:
        gotmode = False
        while not gotmode:
            try:
                print("List of possible coordinates is empty")
                rmode = input("Do you want to reset the list of coordinates? [Y/N]: ")[:1].lower()
                if rmode == "y" or rmode == "n":
                    if rmode == "y":
                        xy = xy2
                    else:
                        continuelist = False
                    gotmode = True
                print()
            except:
                pass

time.sleep(1)
input
