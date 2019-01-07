class CanvasBox:
    def __init__(self,width,height,size,fill_colour,title):
        import tkinter
        self.size = size
        self.width = width
        self.height = height
        self.tkinter = tkinter
        self.points = []
        self.window = tkinter.Tk()
        self.window.title(title)
        self.canvas = tkinter.Canvas(self.window,width=self.width,height=self.height,background=fill_colour)
        self.canvas.grid()

    def update(self):
        self.window.update()

    def clear(self):
        if len(self.points) > 0:
            for i in range(len(self.points)):
                self.canvas.delete(self.points[i])
        self.points = []

    def addPoint(self,x,y,id):
        self.canvas.create_oval(x-(self.size / 2),y-(self.size / 2),x+(self.size / 2),y+(self.size / 2),tags=("Point" + str(id)))
        self.points.append("Point" + str(id))

    def pointColour(self,id,colour,outline_shown,outline_colour="white"):
        if not outline_shown:
            self.canvas.itemconfigure("Point" + str(id), fill=colour)
        else:
            self.canvas.itemconfigure("Point" + str(id), fill=colour, outline=outline_colour)

    def pointColourRGB(self,id,red,green,blue,outline_shown,outline_R=255,outline_G=255,outline_B=255):
        colourHex = "#{:02x}{:02x}{:02x}".format(red,green,blue)
        outline_colourHex = "#{:02x}{:02x}{:02x}".format(outline_R,outline_G,outline_B)
        if not outline_shown:
            self.canvas.itemconfigure("Point" + str(id), fill=colourHex)
        else:
            self.canvas.itemconfigure("Point" + str(id), fill=colourHex, outline=outline_colourHex)
