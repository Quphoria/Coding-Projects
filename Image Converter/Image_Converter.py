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


from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import win32con
from win32api import GetLogicalDriveStrings,GetVolumeInformation
from win32file import GetDriveType

import pickle, os, shutil

global IMDatabase
IMDatabase = []
global rdrives
global gotdb
gotdb = False

def ConvertToText(PILimage):
    #print("Starting Conversion...")
    c_height = PILimage.height
    c_width = PILimage.width

    # File Structure
    #
    # @{Height byte}${Width byte}#{R byte}:{G byte}:{B byte};(Next pixel)!(Next row first pixel);(Next pixel)&
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
    output += bytes([c_height])
    output += "$".encode()
    output += bytes([c_width])
    output += "#".encode()

    for ypixel in range(c_height):
        for xpixel in range(c_width):
            #print((xpixel,ypixel))
            pixeldata = PILimage.getpixel((xpixel,ypixel))
            output += bytes([pixeldata[0]]) + ":".encode() + bytes([pixeldata[1]]) + ":".encode() + bytes([pixeldata[2]])
            if xpixel + 1 < c_width:
                output += ";".encode()
        if ypixel + 1 < c_height:
            output += "!".encode()
    output += "&".encode()
    # print("Conversion Completed Successfully!")
    # print()
    # print(type(output))
    # print("Output")
    # print(output)
    # print()
    return(output)

def ConvertFromText(fodata):
    #print(fodata)
    def invalidfofile():
        raise Exception("Invalid Image")
    globals()["focurrentpos"] = 0
    # fofile = open(fopath,"rb")
    def foread():
        try:
            focp = globals()["focurrentpos"]
            fobyte = fodata[focp]
            globals()["focurrentpos"] += 1
        except Exception as ex:
            print(ex)
            invalidfofile()
        # fobyte = fofile.read(1)
        # if fobyte == b"":
        #     invalidfofile()
        #print(fobyte)
        return fobyte
    def foreadchar(symbol):
        #print(symbol)
        focharbyte = foread()
        if type(focharbyte) != str:
            if chr(focharbyte).encode() != symbol.encode():
                invalidfofile()
        else:
            invalidfofile()
    foreadchar("@")
    #get height and width and verify correct file header
    foheight = int(foread())
    foreadchar("$")
    fowidth = int(foread())

    if not ((fowidth == 32 and foheight == 16) or (fowidth == 16 and foheight == 32)):
        raise Exception("Invalid Size")

    foreadchar("#")

    conimg = PIL.Image.new("RGB",(fowidth,foheight))

    #Read pixels and place them in image and verify correct file structure
    for cury in range(foheight):
        for curx in range(fowidth):
            curr = foread()
            foreadchar(":")
            curg = foread()
            foreadchar(":")
            curb = foread()

            conimg.putpixel((curx,cury),(curr,curg,curb))

            if curx + 1 != fowidth:
                foreadchar(";")
                #print("Pixel Complete")
        if cury + 1 != foheight:
            foreadchar("!")
    foreadchar("&")
    #fofile.close()
    return conimg

globals()["databasepath"] = ""
globals()["databasedrive"] = ""

def createDB(rmdbdrive):
    # IMDatabase = []
    global IMDatabase
    IMDatabase = [[3,"Stripes.png","Stripes.png"],[1,"Dots.jpeg","Dots.png"],[2,"Wave.jpeg","Waves.png"],[4,"Rainbow.png","Rainbow.png"],[5,"Black.png","Black.png"]]
    #IMDatabase = []
    pickle.dump( IMDatabase, open(globals()["databasepath"], "wb" ) )

def loadDB(drname,drpath):
    globals()["databasepath"] = drpath + "\\mximdb.pmdb"
    globals()["databasedrive"] = drpath + "\\"
    global IMDatabase
    if os.path.isfile(globals()["databasepath"]):
        try:
            IMDatabase = pickle.load( open(globals()["databasepath"], "rb" ) )
        except:
            nodatabasewindow(drname,drpath)
    else:
        nodatabasewindow(drname,drpath)
    global gotdb
    gotdb = True



def saveDB():
    ##### Merge changes to actual image files
    pickle.dump( IMDatabase, open(globals()["databasepath"], "wb" ) )



def get_removable_drives(drive_types=(win32con.DRIVE_REMOVABLE,)):
    ret = list([" "])
    drives_str = GetLogicalDriveStrings()
    drives = [item for item in drives_str.split("\x00") if item]
    for drive in drives:
        if GetDriveType(drive) in drive_types:
            try:
                GetVolumeInformation(drive[:2]+"\\")
                ret.append(drive[:2])
            except:
                pass
    #print("Removable Drives: " + str(ret))
    return ret


def nodatabasewindow(drivename,drivepath):
    text1var = "A database was not found on"
    text2var = str(drivename)
    text3var = "Would you like to create a new"
    text4var = "database or select a different SD Card?"

    nodatabasewindowroot = Toplevel()
    nodatabasewindowroot.title(string="No Database Found")
    nodatabasewindowroot.minsize(width=275,height=100)
    nodatabasewindowframe = ttk.Frame(nodatabasewindowroot)
    nodatabasewindowtext1 = ttk.Label(nodatabasewindowframe,text=text1var)
    nodatabasewindowtext1.grid(row=0,column=0,columnspan=2)
    nodatabasewindowtext2 = ttk.Label(nodatabasewindowframe,text=text2var)
    nodatabasewindowtext2.grid(row=1,column=0,columnspan=2)
    nodatabasewindowtext3 = ttk.Label(nodatabasewindowframe,text=text3var)
    nodatabasewindowtext3.grid(row=2,column=0,columnspan=2)
    nodatabasewindowtext4 = ttk.Label(nodatabasewindowframe,text=text4var)
    nodatabasewindowtext4.grid(row=3,column=0,columnspan=2)
    def nodatabasewindownewbuttonfunc():
        createDB(drivepath)
        nodatabasewindowroot.quit()

    nodatabasewindownewbutton = ttk.Button(nodatabasewindowframe,text="Create New Database",command=nodatabasewindownewbuttonfunc)
    nodatabasewindownewbutton.grid(row=4,column=0)
    def nodatabasewindowchangebuttonfunc():
        nodatabasewindowroot.destroy()
    nodatabasewindowchangebutton = ttk.Button(nodatabasewindowframe,text="Change SD Card",command=nodatabasewindowchangebuttonfunc)
    nodatabasewindowchangebutton.grid(row=4,column=1)
    nodatabasewindowframe.pack()
    nodatabasewindowroot.mainloop()
def savedatabasewindow():
    savedatabasewindowroot = Tk()
    savedatabasewindowroot.title(string="Save Database")
    savedatabasewindowroot.minsize(width=245,height=20)
    savedatabasewindowframe = ttk.Frame(savedatabasewindowroot)
    text1var = "Would you like to save the Database?"
    savedatabasewindowtext1 = ttk.Label(savedatabasewindowframe,text=text1var)
    savedatabasewindowtext1.grid(row=0,column=0,columnspan=2)
    def savedatabasewindowyesbuttonfunc():
        saveDB()
        savedatabasewindowroot.destroy()
    savedatabasewindowyesbutton = ttk.Button(savedatabasewindowframe,text="Yes",command=savedatabasewindowyesbuttonfunc)
    savedatabasewindowyesbutton.grid(row=4,column=0)
    def savedatabasewindownobuttonfunc():
        savedatabasewindowroot.destroy()
    savedatabasewindownobutton = ttk.Button(savedatabasewindowframe,text="No",command=savedatabasewindownobuttonfunc)
    savedatabasewindownobutton.grid(row=4,column=1)
    savedatabasewindowframe.grid_rowconfigure(2, minsize=10)
    savedatabasewindowframe.pack()
    savedatabasewindowroot.protocol("WM_DELETE_WINDOW", savedatabasewindowroot.destroy)
    savedatabasewindowroot.mainloop()
def invalidimagewindow(messagetext1,messagetext2):
    invalidimagewindowroot = Toplevel()
    invalidimagewindowroot.title(string="Invalid Image")
    invalidimagewindowroot.minsize(width=250,height=50)
    invalidimagewindowframe = ttk.Frame(invalidimagewindowroot)
    invalidimagewindowtext1 = ttk.Label(invalidimagewindowframe,text=messagetext1)
    invalidimagewindowtext2 = ttk.Label(invalidimagewindowframe,text=messagetext2)
    invalidimagewindowtext1.grid(row=0,column=0)
    invalidimagewindowtext2.grid(row=1,column=0)
    def invalidimagewindowokbuttonfunc():
        invalidimagewindowroot.destroy()

    invalidimagewindowokbutton = ttk.Button(invalidimagewindowframe,text="Ok",command=invalidimagewindowokbuttonfunc)
    invalidimagewindowokbutton.grid(row=3,column=0)

    invalidimagewindowframe.grid_rowconfigure(2, minsize=5)

    invalidimagewindowframe.pack()
    #invalidimagewindowroot.mainloop()

def importDB():
    selimagedb = filedialog.askopenfile(filetypes=(("Image Database","*.pmdb"),("All files","*.*")))
    try:
        IMDatabase = pickle.load( open(selimagedb, "rb" ) )
    except:
        invalidimagewindow("Error: Invalid Database","Unable to import.")

def exportDB():
    selimagedbexp = filedialog.asksaveasfilename(initialfile="mximdb",filetypes=(("Image Database","*.pmdb"),("All files","*.*")))
    try:
        if len(selimagedbexp.split(".")) == 1:
            selimagedbexp += ".pmdb"
        pickle.dump( IMDatabase, open(selimagedbexp, "wb" ) )
    except:
        invalidimagewindow("An Error Occured","Unable to export.")

def DriveSelect():
    def nullfunc(*args):
        print("NullFunc")


    driveselectroot = Tk()

    driveselectroot.title(string="SD Cards")

    context = ttk.Frame(driveselectroot)

    Title = ttk.Label(context,text="Select Target SD Card")
    Title.grid(column=0,row=0,columnspan=3)
    combovar = StringVar()
    InputComboBox = ttk.Combobox(context,textvariable=combovar, state='readonly')
    InputComboBox.grid(column=0,row=1,columnspan=3)


    def refreshdrives(*args):
        global rdrives
        rdrives = get_removable_drives()
        rdrivenames = []
        for i in rdrives:
            rdrivenames.append(i)
        rdrivesfordeletion = []
        for i in range(len(rdrives)):
            try:
                rdrivenames[i] = GetVolumeInformation(rdrivenames[i]+"\\")[0] + " (" + rdrivenames[i] + ")"
            except:
                pass
        #print(rdrivenames)
        InputComboBox['values'] = tuple(rdrivenames)
        if len(rdrivenames) > 1:
            InputComboBox.current(1)
        else:
            InputComboBox.current(0)

    def enterbuttonfunc():
        if InputComboBox["values"][InputComboBox.current()] != " ":
            loadDB(InputComboBox["values"][InputComboBox.current()],rdrives[InputComboBox.current()])
            if gotdb:
                try:
                    driveselectroot.destroy()
                except:
                    pass
    EnterButton = ttk.Button(context,text="Ok",command=enterbuttonfunc)
    EnterButton.grid(column=0,row=2)
    RefreshButton = ttk.Button(context,text="Refresh",command=refreshdrives)
    RefreshButton.grid(column=1,row=2)
    QuitButton = ttk.Button(context,text="Quit",command=sys.exit)
    QuitButton.grid(column=2,row=2)


    context.pack()
    refreshdrives()
    driveselectroot.mainloop()


def EditDatabaseWindow():
    global IMDatabase
    EditDatabaseWindowroot = Tk()

    global imlist
    imlist = {}

    EditDatabaseWindowroot.title(string="Edit Database")

    context = ttk.Frame(EditDatabaseWindowroot)

    def nullfunc(*args):
        print("NullFunc")

    # def toPhotoImage(imfile):
    #     # return ImageTk.PhotoImage(Image.open(imfile))
    #     return ImageTk.PhotoImage(file=imfile)
    def reorder(direction):
        try:
            currentselection = tree.item(tree.focus())["values"][0]
        except:
            direction = 0
            currentselection = 0
        if direction == -1 and currentselection != 1:
            # print("UP")
            currentValue = IMDatabase[currentselection-1]
            IMDatabase[currentselection-1] = IMDatabase[currentselection-2]
            IMDatabase[currentselection-2] = currentValue
            return True
        elif direction == 1 and currentselection != len(IMDatabase):
            # print("DOWN")
            currentValue = IMDatabase[currentselection-1]
            IMDatabase[currentselection-1] = IMDatabase[currentselection]
            IMDatabase[currentselection] = currentValue
            return True
        else:
            return False



    #printbutton = ttk.Button(context,text="Print",width=5,command=nullfunc)
    #printbutton.grid(column=0,row=4)
    def ebutton():
        EditDatabaseWindowroot.destroy()
    exitbutton = ttk.Button(context,text="Exit",command=ebutton)
    exitbutton.grid(column=4,row=4, sticky=(S, E))

    def impbutton():
        importDB()
    importbutton = ttk.Button(context,text="Import",width=10,command=impbutton)
    importbutton.grid(column=2,row=4, sticky=(S, E))
    def expbutton():
        exportDB()
    exportbutton = ttk.Button(context,text="Export",width=10,command=expbutton)
    exportbutton.grid(column=3,row=4, sticky=(S, W))


    dbframe = ttk.Labelframe(context,text="Image Database")

    tree = ttk.Treeview(dbframe, selectmode='browse')

    scrlbr = ttk.Scrollbar(dbframe, orient="vertical", command=tree.yview)


    tree["columns"]=("one","two")
    tree.configure(height=10)
    tree.column('#0', width=75, anchor='nw')
    tree.column("one", width=25, anchor='center')
    tree.column("two", minwidth=150)
    tree.heading('#0', text='Preview')
    tree.heading("one", text="ID")
    tree.heading("two", text="Name")


    def sortIMDB():
        for i in range(len(IMDatabase)):
            IMDatabase[i][0] = i + 1

    sortIMDB()

    def UpdateDBTree():
        tree.delete(*tree.get_children())
        for i in IMDatabase:
            imnum = i[0]
            try:
                imageicon = ConvertFromText(i[2])
                imlist[i[0]] = ImageTk.PhotoImage(imageicon)
                tree.insert("" , i[0]-1, values=(i[0],i[1]), image=imlist[i[0]])
            except Exception as ex:
                print("An exception occured when displaying image " + str(imnum) + ", Error: " + str(ex))
                tree.insert("" , i[0]-1, values=(i[0],i[1]),text = "Error")

    def ubutton():
        if reorder(-1):
            FCTMPID = tree.index(tree.focus())
            sortIMDB()
            UpdateDBTree()
            FCTMPIID = tree.get_children()[FCTMPID-1]
            tree.selection_set([FCTMPIID])
            tree.focus(FCTMPIID)
    upbutton = ttk.Button(context,text="↑",width=3,command=ubutton)
    upbutton.grid(column=0,row=1, sticky=(S))
    def dbutton():
        if reorder(1):
            FCTMPID = tree.index(tree.focus())
            sortIMDB()
            UpdateDBTree()
            FCTMPIID = tree.get_children()[FCTMPID+1]
            tree.selection_set([FCTMPIID])
            tree.focus(FCTMPIID)
    downbutton = ttk.Button(context,text="↓",width=3,command=dbutton)
    downbutton.grid(column=0,row=2, sticky=(N))

    def pbutton():
        if len(IMDatabase) < 100:
            selimagefile = filedialog.askopenfile(filetypes=(("Image Files","*.bmp;*.dib;*.dcx;*.gif;*.im;*.jpg;*.jpe;*.jpeg;*.pcd;*.pcx;*.png;*.pbm;*.pgm;*.ppm;*.psd;*.tif;*.tiff;*.xbm;*.xpm;*.imx"),("All files","*.*")))
            try:
                print(selimagefile.name)
                pfname, pfext = os.path.splitext(selimagefile.name)
                try:
                    if pfext != ".imx":
                        pfimage = PIL.Image.open(selimagefile.name).convert("RGB")
                        if pfimage.width == 32 and pfimage.height == 16:
                            pfdata = ConvertToText(pfimage)
                            IMDatabase.append([-1,os.path.basename(selimagefile.name),pfdata])
                        else:
                            invalidimagewindow("Please make sure the image","resolution is 32x16")
                    else:
                        pffile = open(selimagefile.name,"rb")
                        IMDatabase.append([-1,os.path.basename(selimagefile.name),pffile.read()])
                        pffile.close()
                    sortIMDB()
                    UpdateDBTree()
                except Exception as ex:
                    print(str(ex))
                    invalidimagewindow("Please make sure the file is","a valid image and try again")
                # invalidimagewindow("Please make sure the image","resolution is 32x16")
            except:
                pass

    plusbutton = ttk.Button(context,text="+",width=3,command=pbutton)
    plusbutton.grid(column=0,row=1, sticky=(N))

    def mbutton():
        mindx = tree.index(tree.focus())
        if tree.focus():
            del IMDatabase[mindx]
            sortIMDB()
            UpdateDBTree()
    minusbutton = ttk.Button(context,text="-",width=3,command=mbutton)
    minusbutton.grid(column=0,row=2, sticky=(S))

    context.pack()
    tree.pack(side='left')
    scrlbr.pack(side='right', fill='y')
    dbframe.grid(column=1,row=0,rowspan=4,columnspan=4, sticky=(N, S, E, W))
    UpdateDBTree()

    EditDatabaseWindowroot.mainloop()

def generateImages():
    try:
        genimagefolder = globals()["databasedrive"] + ".imxs/"
        print("Generating Image Files...")
        if not os.path.isdir(genimagefolder):
            os.mkdir(genimagefolder)
        #Delete Old Files
        if os.path.exists(genimagefolder + "imdbsize.dbl"):
            os.remove(genimagefolder + "imdbsize.dbl")
        for i in range(100):
            genfilename = genimagefolder + "imx-" + str(i+1) + ".imx"
            if os.path.exists(genfilename):
                os.remove(genfilename)
        imdbsizefile = open(genimagefolder + "imdbsize.dbl","wb")
        imdbsizefile.write(bytes([len(IMDatabase)]))
        imdbsizefile.close()

        #Generate Files
        for i in range(len(IMDatabase)):
            try:
                imdbgenfile = open(genimagefolder + "imx-" + str(i+1) + ".imx","wb")
                # print(IMDatabase[i][2])
                imdbgenfile.write(IMDatabase[i][2])
                imdbgenfile.close()
            except Exception as ex:
                imdbgenfile.close()
                print("An error occured when generating image " + str(i+1) + ", Error: " + str(ex))
                os.remove(genimagefolder + "imx-" + str(i+1) + ".imx")

    except Exception as ex:
        print("The image files failed to generate, Error: " + str(ex))
        input()

if __name__ == "__main__":
    ######################################    .imx   -- custom image file for matrix
    DriveSelect()
    if gotdb:
        EditDatabaseWindow()
        savedatabasewindow()
        generateImages()
        sys.exit()
        #######Clean up residual temporary files left over from editing
