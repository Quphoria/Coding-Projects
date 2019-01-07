filename = "hashdump.txt"
file = open(filename)
lines = file.readlines()
for line in lines:
    print(line.replace("\n","").split(":")[1])
