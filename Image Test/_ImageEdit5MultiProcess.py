if __name__ == '__main__':
    print("Loading Modules...")


from setuptools.command import easy_install

def install_with_easyinstall(package):
    easy_install.main(["-U", package])


imported = False
tries = 0
while not imported:
    try:
        import socket, importlib
        globals()['PIL'] = importlib.import_module('PIL')

        imported = True
    except Exception as ex:
        print("An error occured when importing PIL: " + str(ex))
        tries += 1
        if tries == 6:
            print("Install Failed.")
            while True:
                pass
        print("Installing PIL... [Try " + str(tries) + "/5]")
        try:
            install_with_easyinstall('Pillow')
            import site, imp
            imp.reload(site)
            print("PIL installed.")
        except Exception as ex:
            print("An error occured when installing PIL: " + str(ex))





import time, math, os, queue #, threading
from multiprocessing import Process, Queue, Value, Manager, Array, cpu_count
globals()["exitFlag"] = False
from tkinter import *
import PIL.Image
from PIL import ImageTk
if __name__ == '__main__':
    print("All Modules Successfully Loaded!")
    #threadnumber = int(cpu_count())
    threadnumber = 1
    #print("Using " + str(threadnumber) + " Thread(s).")
    print("")
    time.sleep(0.5)

def process_data(threadName, q1, q2, im, qlock, ima, rfunc, rerrors, gfunc, gerrors, bfunc, berrors, percent, op, progfname):
    import math

    class shared_data():
        canvas_height = 0
        canvas_width = 0
        x = 0
        y = 0
        progress = 0
        percent = 0
        XValue = 0
        YValue = 0
        red = 0
        green = 0
        blue = 0

    if op == 3:
        data = shared_data()
        import types
        import importlib.machinery
        progloader = importlib.machinery.SourceFileLoader('ImpProgMod', progfname)
        progmod = types.ModuleType(progloader.name)
        progloader.exec_module(progmod)
        rfunc = progmod.redf
        gfunc = progmod.greenf
        bfunc = progmod.bluef
    def funct_if(test,var_true,var_false):
        if (test):
            return var_true
        else:
            return var_false

    def scale(var_old_min, var_old_max, var_new_min, var_new_max, var_value):
        OldSRange = (var_old_max - var_old_min)
        NewSRange = (var_new_max - var_new_min)
        return (((var_value - var_old_min) * NewSRange) / OldSRange) + var_new_min

    def is_even(value_to_test):
        return value_to_test % 2 == 0

    def draw_funct(dfunction, dxmin, dxmax, dymin, dymax, resolution):
        dx = scale(0,canvas_width,dxmin,dxmax,x)
        cdy = eval(dfunction)

        dx = scale(0,canvas_width,dxmin,dxmax,x-resolution)
        pdy = eval(dfunction)

        dx = scale(0,canvas_width,dxmin,dxmax,x+resolution)
        ndy = eval(dfunction)

        cdsy = canvas_height - scale(dymin,dymax,0,canvas_height,cdy)
        pdsy = canvas_height - scale(dymin,dymax,0,canvas_height,pdy)
        ndsy = canvas_height - scale(dymin,dymax,0,canvas_height,ndy)

        dyval = scale(0,canvas_height,dymin,dymax,y)
        py = scale(dymin,dymax,0,canvas_height,dyval-resolution)
        ny = scale(dymin,dymax,0,canvas_height,dyval+resolution)


        #if y - cdsy > py - pdsy and y - cdsy < ny - ndsy:
        #if (cdsy - y < pdsy - y and cdsy - y > ndsy - y) or (cdsy - y > pdsy - y and cdsy - y < ndsy - y):
        if (0 < pdsy - y and 0 > ndsy - y) or (0 > pdsy - y and 0 < ndsy - y) or round(cdsy - y) == 0:
        # print("dx: " + str(dx) + " , dy: " + str(dy))
        # if y - dsy < resolution + 1 and y - dsy > 0-(resolution + 1): #round(dsy) == y:
            return 255
        else:
            return 0


    red = 0
    green = 0
    blue = 0
    canvas_height = im.height
    canvas_width = im.width
    OldXRange = (canvas_width - 0)
    OldYRange = (canvas_height - 0)
    NewRange = (255 - 0)

    def pix2index(xpix,ypix):
        return ((((canvas_height - ypix - 1)*canvas_width) + (xpix)) * 3) - 3

    def getpix(xval,yval):
        pixindex = pix2index(xval,yval)
        try:
            rpix = ima[pixindex]
            gpix = ima[pixindex + 1]
            bpix = ima[pixindex + 2]
        except:
            print("ERROR WITH INDEX: " + str(pixindex))
            while True:
                pass
        return (rpix,gpix,bpix)

    def setpix(xval,yval,val):
        pixindex = pix2index(xval,yval)
        ima[pixindex] = val[0]
        ima[pixindex + 1] = val[1]
        ima[pixindex + 2] = val[2]

    print("[" + str(threadName) + "] Started.")
    # rfunccomp = eval('lambda: ' + globals()["rfunc"], locals())
    # gfunccomp = eval('lambda: ' + globals()["gfunc"], locals())
    # bfunccomp = eval('lambda: ' + globals()["bfunc"], locals())
    while not im.exitFlag:
        gotqdata = False
        #queueLock.acquire()
        if not q1.empty() and im.currq == 1:
            try:
                qlock.acquire()
                datax = q1.get()
                qlock.release()
                gotqdata = True
            except Exception as ex:
                print("Q1Error: " + str(ex))
        elif not q2.empty() and im.currq == 2:
            try:
                qlock.acquire()
                datax = q2.get()
                qlock.release()
                gotqdata = True
            except Exception as ex:
                print("Q2Error: " + str(ex))
        else:
            time.sleep(0.1)
        if gotqdata:
            #queueLock.release()
            #print ("%s processing %s" % (threadName, data))

            x = datax
            #print("[" + str(threadName) + "] Processing " + str(x))
            y = canvas_height
            while y > 0:
                y = y - 1
                qlock.acquire()
                im.tmppix = im.tmppix + 1
                qlock.release()
                #print("Solving: " + str(x) + "," + str(y))
                value = getpix(x,y)

                XValue = round((x * NewRange) / OldXRange)
                YValue = round((y * NewRange) / OldYRange)
                progress = 255 * (percent.value / 100)
                if op == 1:
                    level = round((value[0]+value[1]+value[2]) / 3)
                    pixval = (level,level,level)
                elif op == 2:
                    red = value[0]
                    green = value[1]
                    blue = value[2]

                    try:
                        # r = rfunccomp()
                        r = eval(rfunc, locals())
                    except Exception as ex:
                        print("An Error occured at pixel (" + str(x) + "," + str(y) + "), Colour: " + str(value) + " with the red function: " + rfunc)
                        print("Error: " + str(ex))
                        r = 0
                        rerrors.value = rerrors.value + 1
                    try:
                        # g = gfunccomp()
                        g = eval(gfunc, locals())
                    except Exception as ex:
                        print("An Error occured at pixel (" + str(x) + "," + str(y) + "), Colour: " + str(value) + " with the green function: " + gfunc)
                        print("Error: " + str(ex))
                        g = 0
                        gerrors.value = gerrors.value + 1
                    try:
                        # b = bfunccomp()
                        b = eval(bfunc, locals())
                    except Exception as ex:
                        print("An Error occured at pixel (" + str(x) + "," + str(y) + "), Colour: " + str(value) + " with the blue function: " + bfunc)
                        print("Error: " + str(ex))
                        b = 0
                        berrors.value = berrors.value + 1
                    if r < 0:
                        r = 0
                    if r > 255:
                        r = 255
                    if g < 0:
                        g = 0
                    if g > 255:
                        g = 255
                    if b < 0:
                        b = 0
                    if b > 255:
                        b = 255
                    #print(str(red) + "," + str(green) + "," + str(blue) + ";" + str(r) + "," + str(g) + "," + str(b))
                    pixval = (round(r),round(g),round(b))
                elif op == 3:
                    red = value[0]
                    green = value[1]
                    blue = value[2]

                    data.canvas_height = canvas_height
                    data.canvas_width = canvas_width
                    data.x = x
                    data.y = y
                    data.progress = progress
                    data.percent = percent
                    data.XValue = XValue
                    data.YValue = YValue
                    data.red = red
                    data.green = green
                    data.blue = blue

                    try:
                        # r = rfunccomp()
                        r = rfunc(data)
                    except Exception as ex:
                        print("An Error occured at pixel (" + str(x) + "," + str(y) + "), Colour: " + str(value) + " with the red function: " + str(rfunc))
                        print("Error: " + str(ex))
                        r = 0
                        rerrors.value = rerrors.value + 1
                    try:
                        # g = gfunccomp()
                        g = gfunc(data)
                    except Exception as ex:
                        print("An Error occured at pixel (" + str(x) + "," + str(y) + "), Colour: " + str(value) + " with the green function: " + str(gfunc))
                        print("Error: " + str(ex))
                        g = 0
                        gerrors.value = gerrors.value + 1
                    try:
                        # b = bfunccomp()
                        b = bfunc(data)
                    except Exception as ex:
                        print("An Error occured at pixel (" + str(x) + "," + str(y) + "), Colour: " + str(value) + " with the blue function: " + str(bfunc))
                        print("Error: " + str(ex))
                        b = 0
                        berrors.value = berrors.value + 1
                    if r < 0:
                        r = 0
                    if r > 255:
                        r = 255
                    if g < 0:
                        g = 0
                    if g > 255:
                        g = 255
                    if b < 0:
                        b = 0
                    if b > 255:
                        b = 255
                    #print(str(red) + "," + str(green) + "," + str(blue) + ";" + str(r) + "," + str(g) + "," + str(b))
                    pixval = (round(r),round(g),round(b))
                else:
                    pixval = value
                # print("Changing pixel (" + str(x) + "," + str(y) + ") from " + str(value) + " to " + str(pixval))
                #print("Before: " + str(x) + "," + str(y) + ":" + str(getpix(x,y)))
                setpix(x,y,pixval)
                #print("After: " + str(x) + "," + str(y) + ":" + str(getpix(x,y)))
        else:
            #queueLock.release()
            pass
            #time.sleep(1)
    print("[" + str(threadName) + "] Exiting.")


if __name__ == '__main__':
    threadnumber = 1
    got_threads = False
    while not got_threads:
        try:
            threads = int(input("Number of threads: "))
            if threads > 0 and threads <= 256:
                got_threads = True
                threadnumber = threads
            else:
                print("Please enter a number between 1 and 256")
        except:
            print("Please enter a number between 1 and 256")
    print("Using " + str(threadnumber) + " Thread(s).")
    progfilename = ""
    print("""Modes:
    0: Generate New Image
    1: Load Image from File
    """)
    source = 0
    gotsource = False
    while not gotsource:
        try:
            source = int(input("Mode: "))
            if source == 0 or source == 1:
                gotsource = True
            else:
                print("Please enter either 0 or 1")
        except:
            print("Please enter either 0 or 1")



    print("")
    if source == 0:
        genapproved = ""
        while not genapproved.lower() == "y":
            print("")
            gotdimensions = False
            while not gotdimensions:
                try:
                    genheight = int(input("Image Height in Pixels: "))
                    genwidth = int(input("Image Width in Pixels: "))
                    if genheight > 0 and genwidth > 0:
                        gotdimensions = True
                    else:
                        print("Please enter a valid integer")
                except:
                    print("Please enter a valid integer")
            filename = input("Image name: ")
            genapproved = input("Are these settings correct? [Y/N]: ")
        print("")
        print("Generating Canvas...")
        try:
            im = PIL.Image.new("RGB",(genwidth,genheight))
        except Exception as ex:
            print("An error occured when generating a canvas")
            print("Error: " + str(ex))
            while True:
                pass
        time.sleep(1)
        print("Canvas Generated Successfully")


    elif source == 1:
        imported = False
        while not imported:
            try:
                filename = input("Image Filename: ")
                im = PIL.Image.open(filename)
                imported = True
            except Exception as ex:
                print("An error occured when importing the image: " + str(ex))
    else:
        print("An Error Occured With Setting The Mode")
        while True:
            pass
    print("""Operations:
    0: Nothing
    1: Greyscale
    2: Custom
    3: Custom program from file
    """)

    opsuccess = False
    while not opsuccess:
        try:
            op = int(input("Operation: "))
            if 0 <= op and op <= 3:
                opsuccess = True
            else:
                print("Invalid Op Code")
        except:
            print("Invalid Op Code")

    canvas_height = im.height
    canvas_width = im.width
    progress = 0
    percent = 0
    XValue = 0
    YValue = 0
    x = 0
    y = 0


    print("")
    print("Image Dimensions")
    print("Height: " + str(canvas_height))
    print("Width: " + str(canvas_width))
    print("")

    if op == 0:
        rfunc = "red"
        gfunc = "green"
        bfunc = "blue"
    elif op == 1:
        rfunc = "round((red+green+blue) / 3)"
        gfunc = "round((red+green+blue) / 3)"
        bfunc = "round((red+green+blue) / 3)"
    elif op == 3:
        sfile = ""
        gotfile = False
        while not gotfile:
            try:
                print()
                sfile = input("File: ")
                f = open(sfile,'rb')
                f.close()
                gotfile = True
            except Exception as ex:
                print("An error occured when opening the file: " + str(ex))
                if sfile == "":
                    sys.exit()
        print("File: " + sfile)
        progfilename = sfile
        rfunc = ""
        gfunc = ""
        bfunc = ""
    elif op == 2:
        cusapproved = ""
        while cusapproved.lower() != "y" :
            print("""
    Available Varibles:
    canvas_height
    canvas_width
    x
    y
    progress
    percent
    XValue
    YValue
    red
    green
    blue

    Available Functions:
    Anything from the math module
    funct_if(thing to test,value if true, value if false)
    scale(value minimum, value maximum, new minimum, new maximum, value)
    is_even(value)
    draw_funct(function(use dx instead of x and put in quotation marks), x value minimum, x value maximum, y value minimum, y value maximum, resolution in px)
    """)
            globals()["rfunc"] = str(input("Red function: "))
            globals()["gfunc"] = str(input("Green function: "))
            globals()["bfunc"] = str(input("Blue function: "))
            cusapproved = input("Are these functions correct? [Y/N]: ")

        x = 0
        y = 0
        pix = 0



    tmpx = 0

    OldXRange = (im.width - 0)
    OldYRange = (im.height - 0)
    NewRange = (255 - 0)


    print("Starting Conversion...")
    starttime = time.time()
    manager = Manager()


    #threadList = ["Thread-1", "Thread-2", "Thread-3"]
    #queueLock = threading.Lock()
    # workQueue = queue.Queue(50000)
    workQueue1 = manager.Queue(2500)
    workQueue2 = manager.Queue(2500)
    threads = []
    threadID = 1
    threadnum = threadnumber

    imlist = list(im.tobytes())

    #ima = list(im.getdata())

    mcim = manager.Namespace()
    mcim.exitFlag = False
    mcim.tmppix = 0
    mcim.currq = 200
    mcim.height = im.height
    mcim.width = im.width
    mcqlock = manager.Lock()
    mcima = Array("i",imlist)
    rerrors = Value('d', 0)
    gerrors = Value('d', 0)
    berrors = Value('d', 0)
    percent = Value('d', 0)


    # Create new threads
    print("Starting Processes...")
    for tNum in range(threadnum):
        #thread = myThread(threadID, "Thread-" + str(threadID), workQueue)
        # process_data(threadName, q, im, exitFlag, tmppix, rfunc, rerrors, gfunc, gerrors, bfunc, berrors, percent)
        thread = Process(target=process_data, args=("Process-" + str(threadID), workQueue1 , workQueue2, mcim, mcqlock, mcima, rfunc, rerrors, gfunc, gerrors, bfunc, berrors, percent, op, progfilename,))
        thread.start()
        threads.append(thread)
        threadID += 1


    status = Tk()

    status.title(string = "Status")

    percentchange = 0
    totalpix = im.width * im.height
    time.sleep(1)
    pixtmp = 0
    print("Allocating Pixels...")
    mcim.currq = 2
    while tmpx < im.width:
        while (workQueue1.full() and workQueue2.full()) and not (workQueue1.empty() and workQueue2.empty()):
            print("FULL: " + str(workQueue1.full() and workQueue2.full()))
            print("EMPTY: " + str(not (workQueue1.empty() and workQueue2.empty())))
        if workQueue1.full() and workQueue2.empty():
            mcim.currq = 1
            print("Q1")
        elif workQueue2.full() and workQueue1.empty():
            mcim.currq = 2
            print("Q2")
        elif (mcim.currq == 1 and workQueue2.full()) or (mcim.currq == 2 and workQueue1.full()):
            time.sleep(0.5)
        else:
            pass

        try:
            if mcim.currq == 1:
                workQueue2.put(tmpx)
            elif mcim.currq == 2:
                workQueue1.put(tmpx)
            else:
                print("invalid currq")
            pixtmp += 1
        except:
            print("put error")
        print(str(pixtmp) + "/" + str(im.width))

        oldpercent = percent.value
        percentl = (mcim.tmppix - 1) / (totalpix / 100)
        percent.value = round(percentl,1)
        if oldpercent != percent.value:
            Label(status,text = (str(percent.value) + "%"), anchor="w").grid(row = 1, column = 1)
            status.update()
        tmpx = tmpx + 1


    print("Finished allocating pixels")

    while mcim.tmppix != totalpix:
        if workQueue1.empty() and not workQueue2.empty():
            mcim.currq = 2
        elif not workQueue1.empty() and workQueue2.empty():
            mcim.currq = 1
        oldpercent = percent.value
        percentl = (mcim.tmppix - 1) / (totalpix / 100)
        percent.value = round(percentl,1)
        if oldpercent != percent.value:
            Label(status,text = (str(percent.value) + "%"), anchor="w").grid(row = 1, column = 1)
            status.update()
        time.sleep(0.1)
        print("Queue Size: " + str(workQueue1.qsize() + workQueue2.qsize()) + " , ExitFlag: " + str(mcim.exitFlag) + " , " + str(mcim.tmppix) + "/" + str(totalpix) + " , QSIZE+TMPPIX: " + str((workQueue1.qsize() + workQueue2.qsize())*im.height + mcim.tmppix))
    mcim.exitFlag = True
    print("Stopping Processes...")
    for t in threads:
        t.join()

    Label(status,text = (str(100.0) + "%"), anchor="w").grid(row = 1, column = 1)
    status.update()

    #imoutput = mcim.im
    imoutput = PIL.Image.new(im.mode,im.size)
    imoutput.frombytes(bytes(mcima))

    endtime = time.time()
    processtime = endtime - starttime
    s2m = divmod(processtime, 60)
    m2h = divmod(s2m[0], 60)
    timeseconds = round(s2m[1],3)
    timeminutes = round(m2h[1])
    timehours = round(m2h[0])

    print("Conversion Completed Successfully in " + str(timehours) + " hours, " + str(timeminutes) + " minutes and " + str(timeseconds) + " seconds.")
    time.sleep(0.5)
    print()
    print("Conversion Summary:")
    time.sleep(0.5)
    print("Your Red Function: Red = " + str(rfunc) + " had " + str(rerrors.value) + " error(s).")
    time.sleep(0.5)
    print("Your Green Function: Green = " + str(gfunc) + " had " + str(gerrors.value) + " error(s).")
    time.sleep(0.5)
    print("Your Blue Function: Blue = " + str(bfunc) + " had " + str(berrors.value) + " error(s).")
    print("")
    time.sleep(1)
    print("Saving...")
    savid = 0
    saved = False
    while not saved:
        if not os.path.isfile(filename + "-" + str(savid) + "sav.png"):
            imoutput.save(filename + "-" + str(savid) + "sav.png", "PNG")
            saved = True
        else:
            savid = savid + 1
    print("Saved as: " + filename + "-" + str(savid) + "sav.png")
    status.destroy()

    root = Tk()

    photo = ImageTk.PhotoImage(imoutput)

    canvas = Canvas(width=canvas_width, height=canvas_height, bg='white')
    canvas.pack()
    canvas.create_image(canvas_width/2, canvas_height/2, image=photo)

    root.mainloop()

    while True:
        pass
