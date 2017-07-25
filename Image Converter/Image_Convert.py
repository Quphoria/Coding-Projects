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

import PIL.Image
from PIL import ImageTk
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import time, math, os, queue, threading, codecs
exitFlag = 0
from tkinter import *
from tkinter import filedialog
print("All Modules Successfully Loaded!")
print("")
time.sleep(0.5)

gotfile = False
while not gotfile:
    try:
        print()
        #sfile = input("File: ")
        root = Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(initialdir=os.getcwd())
        globals()["im"] = PIL.Image.open(filename)
        gotfile = True
    except Exception as ex:
        print("An error occured when opening the image: " + str(ex))
        if filename == "":
            sys.exit()
print("File: " + filename)

canvas_height = globals()["im"].height
canvas_width = globals()["im"].width

# root = Tk()
#
# photo = ImageTk.PhotoImage(globals()["im"])
#
# canvas = Canvas(width=canvas_width, height=canvas_height, bg='black')
# canvas.pack()
# canvas.create_image(canvas_width/2, canvas_height/2, image=photo)
#
# root.mainloop()

def ConvertToText(PILimage):
    print("Starting Conversion...")
    c_height = PILimage.height
    c_width = PILimage.width

    # File Structure
    # rcc - raw character code (raw value stored as 1 character)
    #
    # @{Height rcc}${Width rcc}#{R rcc}:{G rcc}:{B rcc};(Next pixel)!(Next row first pixel);(Next pixel)&
    #
    # @ next char height
    # $ next char width
    # # next char starting pixel
    # : colour seperator
    # ; pixel seperator
    # ! row seperator
    # & EOF
    # Bottom left LED 0,0

    output = "@".encode()
    # output += bytes(chr(c_height))
    output += bytes([c_height])
    output += "$".encode()
    # output += bytes(chr(c_width))
    output += bytes([c_width])
    output += "#".encode()

    for ypixel in range(0,c_height):
        for xpixel in range(0,c_width):
            print((xpixel,ypixel))
            pixeldata = PILimage.getpixel((xpixel,ypixel))
            # output += bytes(chr(pixeldata[0])) + ":".encode() + bytes(chr(pixeldata[1])) + ":".encode() + bytes(chr(pixeldata[2]))
            output += bytes([pixeldata[0]]) + ":".encode() + bytes([pixeldata[1]]) + ":".encode() + bytes([pixeldata[2]])
            if xpixel + 1 < c_width:
                output += ";".encode()
        if ypixel + 1 < c_height:
            output += "!".encode()
    output += "&".encode()
    print("Conversion Completed Successfully!")
    print()
    print(type(output))
    print("Output")
    print(output)
    print()
    return(output)

imageText = ConvertToText(globals()["im"])
time.sleep(1)
print("Saving...")
savid = 0
saved = False
while not saved:
    if not os.path.isfile(filename + "-" + str(savid) + ".txpic"):
        #cfile = codecs.open(filename=filename + "-" + str(savid) + ".txpic",mode="w+",encoding=None)
        cfile = open(filename + "-" + str(savid) + ".txpic", "wb")
        cfile.write(imageText)
        cfile.close()
        saved = True
    else:
        savid = savid + 1
print("Saved as: " + filename + "-" + str(savid) + ".txpic")

input()
