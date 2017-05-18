globals()["inp"] = 1

def getinput():
    dt = input("Enter Value " + str(globals()["inp"]) + ": ")
    globals()["inp"] = globals()["inp"] + 1
    return dt

def output(odat):
    print("Output: \'" + str(odat) + "\'")

def torail(tor):
    r1 = ""
    r2 = ""
    rn = 1
    for j in tor:
        if rn == 1:
            r1 = r1 + j
            rn = 2
        else:
            r2 = r2 + j
            rn = 1
    return (r1,r2)

def fromrail(r1,r2):
    tlen = len(r1) + len(r2)
    rout = ""
    r1pos = 0
    r2pos = 0
    while len(rout) < tlen:
        er = 0
        if len(r1) > r1pos:
            rout = rout + r1[r1pos]
            r1pos = r1pos + 1
        else:
            er = 1
        if len(r2) > r2pos:
            rout = rout + r2[r2pos]
            r2pos = r2pos + 1
        elif er == 1:
            print("[fromrail] Error Out of Characters")
    return rout

def toshift(tst, tsn):
    sout = ""
    charnum = 0
    for schr in tst:
        charnum = charnum + 1
        if schr.isalpha():
            schc = ord(schr) + eval(str(tsn))
            valid = False
            while not valid:
                if schr.isupper():
                    if schc > ord("Z"):
                        schc = schc - 26
                    elif schc < ord("A"):
                        schc = schc + 26
                    else:
                        valid = True
                elif schr.islower():
                    if schc > ord("z"):
                        schc = schc - 26
                    elif schc < ord("a"):
                        schc = schc + 26
                    else:
                        valid = True
            sout = sout + chr(schc)
        else:
            sout = sout + schr
    return sout

def fromshift(tst, tsn):
    sout = ""
    charnum = 0
    for schr in tst:
        charnum = charnum + 1
        if schr.isalpha():
            schc = ord(schr) - eval(str(tsn))
            valid = False
            while not valid:
                if schr.isupper():
                    if schc > ord("Z"):
                        schc = schc - 26
                    elif schc < ord("A"):
                        schc = schc + 26#
                    else:
                        valid = True
                elif schr.islower():
                    if schc > ord("z"):
                        schc = schc - 26
                    elif schc < ord("a"):
                        schc = schc + 26
                    else:
                        valid = True
            sout = sout + chr(schc)
        else:
            sout = sout + schr
    return sout

def bfshift(bft):
    for i in range(26):
        gss = toshift(bft, i)
        print(str(i) + " : \'" + str(gss) + "\'")

def toshiftascii(tst, tsn):
    sout = ""
    charnum = 0
    for schr in tst:
        charnum = charnum + 1
        try:
            setl = False
            if ord(schr) < 127:
                setl = True
            schc = ord(schr) + eval(str(tsn))
            valid = False
            while not valid:
                if setl:
                    if schc > ord("~"):
                        schc = schc - 95
                    elif schc < ord(" "):
                        schc = schc + 95
                    else:
                        valid = True
                elif not setl:
                    if schc > 255:
                        schc = schc - 128
                    elif schc < 128:
                        schc = schc + 128
                    else:
                        valid = True
            sout = sout + chr(schc)
        except Exception as ex:
            print("Error with Character :\'" + str(schr) + "\' : " + str(ex))
            sout = sout + schr
    return sout

def fromshiftascii(tst, tsn):
    sout = ""
    charnum = 0
    for schr in tst:
        charnum = charnum + 1
        try:
            setl = False
            if ord(schr) < 127:
                setl = True
            schc = ord(schr) - eval(str(tsn))
            valid = False
            while not valid:
                if setl:
                    if schc > ord("~"):
                        schc = schc - 95
                    elif schc < ord(" "):
                        schc = schc + 95
                    else:
                        valid = True
                elif not setl:
                    if schc > 255:
                        schc = schc - 128
                    elif schc < 128:
                        schc = schc + 128
                    else:
                        valid = True
            sout = sout + chr(schc)
        except Exception as ex:
            print("Error with Character :\'" + str(schr) + "\' : " + str(ex))
            sout = sout + schr
    return sout


def run():
    gotprogram = False
    while not gotprogram:
        try:
            fn = input("Enter PROG file name: ")
            opfile = open(fn, "r")
            gotprogram = True
        except:
            print("Error Opening File. Please Try Again.")
    data = opfile.readlines()
    opfile.close()
    for i in data:
        exec(i)

if __name__ == "__main__":
    try:
        run()
        print("Completed")
    except Exception as ex:
        print("An Error Occured: " + str(ex))
    while True:
        pass
