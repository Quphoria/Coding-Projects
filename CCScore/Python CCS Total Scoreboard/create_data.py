base = "T-"
team_number = 25

import random

csvfile = open("data.csv","w")
csvfile.write("ID,Points\n")

for i in range(1,team_number):
    csvfile.write(base + str(i) + "," + str(random.randrange(0,100)) + "\n")
csvfile.close()
