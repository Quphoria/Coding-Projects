import random, time, os

def Validate(lista,listb):
    Valid = True
    if len(lista) == len(listb):
        for listindex in range(len(lista)):
            if lista[listindex] == listb[listindex]:
                Valid = False
    else:
        Valid = False
    return(Valid)

os.system("color c")

assignvalid = False
while not assignvalid:
    symbollist = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    print(symbollist)
    random.shuffle(symbollist)
    print(symbollist)
    assignlist = []
    shiftamount = random.randint(1,len(symbollist)-1)
    for index in range(len(symbollist)):
        if index - shiftamount < 0:
            assignlist.append(symbollist[len(symbollist) + index - shiftamount])
        else:
            assignlist.append(symbollist[index - shiftamount])
    print(assignlist)
    assignvalid = Validate(symbollist,assignlist)
    if assignvalid:
        os.system("color a")
    else:
        os.system("color c")
    print("List Valid: " + str(assignvalid))
    assigneddict = {}
    for index in range(len(symbollist)):
        assigneddict[symbollist[index]] = assignlist[index]
    print(assigneddict)
    print()
    time.sleep(0.1)
