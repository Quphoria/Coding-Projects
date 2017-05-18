import sys
def solver():
    print("")
    print("-------------------------------")
    print("")
    print("1 | Number of Terms")
    print("2 | Last Term")
    print("3 | Sum of Terms")
    option = input("Option: ")
    if option == "quit" or option == "exit":
        sys.exit()
    try:
        option = int(option)
    except Exception as ex:
        raise Exception("Unknown Option")
    if option == 1 or option == 2 or option == 3:
        a = input("1st Term= ")
        if str(a).lower() == "quit" or str(a).lower() == "exit":
            sys.exit()
        else:
            a = float(a)
        b = float(input("2nd Term= "))
        
    if option == 1:
        c = float(input("Number of Terms= "))
    elif option == 2:
        last = float(input("Last Term= "))
    elif option == 3:
        total_sum = float(input("Sum of Terms= "))
        
    if option == 1 or option == 2 or option == 3:
        diff = b - a
        offset = a - diff
        
    if option == 1:
        last = (diff * c) + offset
    elif option == 2:
        not_offset_last = last - offset
        c = not_offset_last / diff
    elif option == 3:
        terms = 0
        while (total_sum != 0 or terms == 0) and terms < 1000000:
            terms = terms + 1
            total_sum = total_sum - ((diff * terms) + offset)
        if total_sum < 0:
            ans = "Invalid Total"
        else:
            ans = terms
        
    if option == 1 or option == 2:
        first_plus_last = a + last
        ans = (c * first_plus_last) / 2
    if option == 1 or option == 2 or option == 3:
        print("Answer = " + str(ans))
    else:
        raise Exception("Unknown option")
while True:
    try:
        solver()
    except Exception as ex:
        print("An error occured: " + str(ex))
