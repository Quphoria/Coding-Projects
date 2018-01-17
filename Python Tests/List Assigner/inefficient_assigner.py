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
namelist = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
assignvalid = False
while not assignvalid or True:
    symbollist = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    print(namelist)
    random.shuffle(symbollist)
    print(symbollist)
    assignvalid = Validate(namelist,symbollist)
    if assignvalid:
        os.system("color a0")
    else:
        os.system("color c0")
    print("List Valid: " + str(assignvalid))
    assigneddict = {}
    for index in range(len(namelist)):
        assigneddict[namelist[index]] = symbollist[index]
    print(assigneddict)
    print()
    time.sleep(0.1)
