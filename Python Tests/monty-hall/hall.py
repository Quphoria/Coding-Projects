import random

master_doors = ["real","fake","fake"]

stay = 0
swap = 0

n = 0
while n < 100000:
    n += 1
    doors = master_doors.copy()
    random.shuffle(doors)
    door = random.randrange(0,3)
    temp_doors = doors.copy()
    temp_doors[door] = "chosen"
    fake_door = temp_doors.index("fake")
    if doors[door] == "real":
        stay += 1
    else:
        swap += 1
    print("Stay: %s    Swap: %s    Stay%%: %s%%    Swap%%: %s%%" % (stay,swap,int((stay/(stay+swap))*100),int((swap/(stay+swap))*100)))