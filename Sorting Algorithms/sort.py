quicksort_version = 2
try:
    import time
    def infwait():
        print()
        print("The program has finished.")
        while True:
            time.sleep(1)
except Exception as ex:
    print("An error occured when loading the time module or initialising: " + str(ex))
try:
    import os
    import plugins
    import bubble
    import merge
    import verify
    if quicksort_version == 1:
        import quicksort
    elif quicksort_version == 2:
        import quicksort2 as quicksort
    else:
        raise ImportWarning("Invalid quicksort version")
except Exception as ex:
    print("An error occured when importing: " + str(ex))
    infwait()


gotlist = False
while not gotlist:
    try:
        lf = input("File containing list of numbers (seperated with spaces): ")
        lfo = open(lf, "r")
        data = lfo.read()
        lfo.close()
        nlist = data.split(" ")
        gotlist = True
    except Exception as ex:
        print("An error occured when opening the file: " + str(ex))
print("Length of list to sort: " + str(len(nlist)))

gotalg = False
while not gotalg:
    print()
    print("Sorting Algorithms:")
    print("[0] Bubble Sort")
    print("[1] Merge Sort")
    print("[2] Quicksort")
    print("[3] Verify Sort")
    print()
    try:
        op = int(input("Enter Algorithm [0-3]: "))
        if op >= 0 and op < 4:
            gotalg = True
        else:
            print("Please enter a valid algorithm number.")
            print()
    except:
        print("Please enter a valid algorithm number.")
gotorder = False
while not gotorder:
    print()
    print("Order:")
    print("[0] Low to High")
    print("[1] High to low")
    print()
    try:
        order = int(input("Enter Order [0-1]: "))
        if order >= 0 and order < 2:
            gotorder = True
        else:
            print("Please enter a valid order number.")
            print()
    except:
        print("Please enter a valid order number.")
if op == 0:
    algname = "Bubble Sort"
elif op == 1:
    algname = "Merge Sort"
elif op == 2:
    algname = "Quicksort"
else:
    algname = "INVALID"
if order == 0:
    ordername = "Lowest to Highest"
elif order == 1:
    ordername = "Highest to Lowest"
else:
    ordername = "INVALID"

if op != 3:
    print("Sorting from " + ordername + " with " + algname +"...")
else:
    print("Verifying sort from " + ordername + "...")
starttime = time.time()
try:
    if op == 0:
        olist = bubble.sort(nlist)
    elif op == 1:
        olist = merge.sort(nlist)
    elif op == 2:
        olist = quicksort.sort(nlist)
    elif op == 3:
        valid_sort = verify.check(nlist,order)
    else:
        print("Invalid Operation Sort Error")
        olist = nlist
    endtime = time.time()
    totaltime = endtime - starttime
    if op != 3:
        if order == 1:
            olist = plugins.reverse(olist)
        print("Sorted in: " + str(totaltime) + " seconds")
    elif valid_sort:
        print("Verified in: " + str(totaltime) + " seconds")
    else:
        print ("Failed Verification in: " + str(totaltime) + " seconds")
    if op != 3:
        olist = plugins.remove_dp(olist)
        for i in range(len(olist)):
            if i == 0:
                olist[i] = str(olist[i])
            else:
                olist[i] = " " + str(olist[i])
    time.sleep(1)
except Exception as ex:
    if op != 3:
        print("An error occured when sorting: " + str(ex))
    else:
        print("An error occured when verifying: " + str(ex))
    infwait()
if op != 3:
    try:
        print()
        print("Saving...")
        savid = 0
        saved = False
        while not saved:
            if not os.path.isfile(lf + "-" + str(savid) + "sorted.txt"):
                ofile = open(lf + "-" + str(savid) + "sorted.txt", "w")
                for i in range(len(olist)):
                    ofile.write(olist[i])
                ofile.close()
                saved = True
            else:
                savid = savid + 1
        print("Saved as: " + lf + "-" + str(savid) + "sorted.txt")
    except Exception as ex:
        print("An error occured when saving: " + str(ex))
        infwait()
infwait() # EOF
