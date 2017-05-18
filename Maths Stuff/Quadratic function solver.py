import sys
from math import sqrt
def solver():
    print("")
    print("-------------------------------")
    print("")
    print("format = ax^2 + bx + c")
    a = input("a= ")
    if str(a).lower() == "quit" or str(a).lower() == "exit":
        sys.exit()
    else:
        a = float(a)
    b = float(input("b= "))
    c = float(input("c= "))
    d = sqrt((b*b)-(4*a*c))
    ans1 = (0-b+d)/(2*a)
    ans2 = (0-b-d)/(2*a)
    print("Answer 1 = " + str(ans1))
    print("Answer 2 = " + str(ans2))
while True:
    try:
        solver()
    except Exception as ex:
        print("An error occured: " + str(ex))
