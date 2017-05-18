print("Loading Modules...")

print("Importing time...")
import time
time.sleep(0.1)
print("Importing math...")
import math
time.sleep(0.1)
print("Importing os...")
import os
time.sleep(0.1)
print("Importing tkinter...")
from tkinter import *
time.sleep(0.1)
print("Importing PIL.image...")
import PIL.Image
time.sleep(0.1)
print("Importing ImageTk from PIL...")
from PIL import ImageTk
time.sleep(0.1)
print("All Modules Successfully Loaded!")
print("")
time.sleep(0.5)

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
""")

opsuccess = False
while not opsuccess:
    try:
        op = int(input("Operation: "))
        if 0 <= op and op <= 2:
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
red = 0
green = 0
blue = 0
x = 0
y = 0

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
    dy = eval(dfunction)
    dsy = canvas_height - scale(dymin,dymax,0,canvas_height,dy)
    # print("dx: " + str(dx) + " , dy: " + str(dy))
    if y - dsy < resolution + 1 and y - dsy > 0-(resolution + 1): #round(dsy) == y:
        return 255
    else:
        return 0

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
        rfunc = str(input("Red function: "))
        gfunc = str(input("Green function: "))
        bfunc = str(input("Blue function: "))
        cusapproved = input("Are these functions correct? [Y/N]: ")

    rfunccomp = eval('lambda: ' + rfunc)
    gfunccomp = eval('lambda: ' + gfunc)
    bfunccomp = eval('lambda: ' + bfunc)

x = 0

OldXRange = (im.width - 0)
OldYRange = (im.height - 0)
NewRange = (255 - 0)



print("Starting Conversion...")

rerrors = 0
gerrors = 0
berrors = 0

status = Tk()

status.title(string = "Status")

percent = 0
percentchange = 0

pix = 0
totalpix = im.width * im.height / 100
while x < im.width:
    y = 0
    while y < im.height:
        value = im.getpixel((x,y))
        XValue = round((x * NewRange) / OldXRange)
        YValue = round((y * NewRange) / OldYRange)
        progress = 255 * (percent / 100)
        if op == 1:
            level = round((value[0]+value[1]+value[2]) / 3)
            pixval = (level,level,level)
        elif op == 2:
            red = value[0]
            green = value[1]
            blue = value[2]
            try:
                r = rfunccomp()
            except Exception as ex:
                print("An Error occured at pixel (" + str(x) + "," + str(y) + "), Colour: " + str(value) + " with the red function: " + rfunc)
                print("Error: " + str(ex))
                r = 0
                rerrors = rerrors + 1
            try:
                g = gfunccomp()
            except Exception as ex:
                print("An Error occured at pixel (" + str(x) + "," + str(y) + "), Colour: " + str(value) + " with the green function: " + gfunc)
                print("Error: " + str(ex))
                g = 0
                gerrors = gerrors + 1
            try:
                b = bfunccomp()
            except Exception as ex:
                print("An Error occured at pixel (" + str(x) + "," + str(y) + "), Colour: " + str(value) + " with the blue function: " + bfunc)
                print("Error: " + str(ex))
                b = 0
                berrors = berrors + 1
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
            pixval = (round(r),round(g),round(b))
        else:
            pixval = value
        #print("Changing pixel (" + str(x) + "," + str(y) + ") from " + str(value) + " to " + str(pixval))
        im.putpixel((x,y),pixval)
        y = y + 1
        pix = pix + 1

        oldpercent = percent
        percent = (pix - 1) / totalpix
        percent = round(percent,1)
        if oldpercent != percent:
            Label(status,text = (str(percent) + "%"), anchor="w").grid(row = 1, column = 1)
            status.update()
    x = x + 1

print("Conversion Completed Successfully!")
time.sleep(0.5)
print("""
Conversion Summary:""")
time.sleep(0.5)
print("Your Red Function: Red = " + str(rfunc) + " had " + str(rerrors) + " error(s).")
time.sleep(0.5)
print("Your Green Function: Green = " + str(gfunc) + " had " + str(gerrors) + " error(s).")
time.sleep(0.5)
print("Your Blue Function: Blue = " + str(bfunc) + " had " + str(berrors) + " error(s).")
print("")
time.sleep(1)
print("Saving...")
savid = 0
saved = False
while not saved:
    if not os.path.isfile(filename + "-" + str(savid) + "sav.png"):
        im.save(filename + "-" + str(savid) + "sav.png", "PNG")
        saved = True
    else:
        savid = savid + 1
print("Saved as: " + filename + "-" + str(savid) + "sav.png")
status.destroy()

root = Tk()

photo = ImageTk.PhotoImage(im)

canvas = Canvas(width=canvas_width, height=canvas_height, bg='white')
canvas.pack()
canvas.create_image(canvas_width/2, canvas_height/2, image=photo)

root.mainloop()

while True:
    pass
