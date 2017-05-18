import random
gotlength = False
while not gotlength:
    try:
        listlength = input("Please enter desired list length: ")
        llen = int(listlength)
        if llen > 0:
            gotlength = True
        else:
            print("Please enter a valid integer above 0")
    except:
        print("Please enter a valid integer above 0")
gotmode = False
while not gotmode:
    try:
        listmode = input("Please enter desired amount of decimal places: ")
        lmode = 10**int(listmode)
        if lmode > 0:
            gotmode = True
        else:
            print("Please enter a valid integer that is 0 or higher")
    except:
        print("Please enter a valid integer that is 0 or higher")
try:
    numlist = []
    print("Creating List...")
    for i in range(llen):
        numlist.append(str((i + 1) / lmode))
    print("List Created")
    print("Shuffling List...")
    random.shuffle(numlist)
    print("List Shuffled")
    print("Preparing List for Saving...")
    for i in range(len(numlist)):
        if i != 0:
            numlist[i] = " " + numlist[i]
    print("List Prepared for Saving")
except Exception as ex:
    print("An erro occured when creating the list: " + str(ex))
    while True:
        pass

saved = False
while not saved:
    try:
        lname = input("Please enter the filename that you want to save the list as: ")
        print("Saving...")
        sfile = open(lname, "w")
        for i in range(len(numlist)):
            sfile.write(numlist[i])
        sfile.close()
        saved = True
        print("Saved as: " + lname)
    except Exception as ex:
        print("An error occured when saving, this could be due to an invalid filename, Please try saving again.")
        print("Error: " + str(ex))
while True:
    pass
