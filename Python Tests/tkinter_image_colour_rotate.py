import tkinter, PIL, numpy
from PIL import Image, ImageTk, ImageColor

ImageName = "rndn-0sav.png"# input("Image: ")

def hue_shift(hsvarr, amount):
    hsv[..., 0] = (hsvarr[..., 0]+amount) % 360
    new_img = Image.fromarray(hsv, 'HSV')
    return new_img.convert('RGB')

window = tkinter.Tk()
PILImage = Image.open(ImageName)
print(PILImage.width)
print(PILImage.height)
hsv_img = PILImage.convert('HSV')
hsv = numpy.array(hsv_img)

canvas = tkinter.Canvas(width=PILImage.width, height=PILImage.height, bg='white')
canvas.pack()

hue = 0
while True:
    IM2 = hue_shift(hsv,hue)
    photo = ImageTk.PhotoImage(IM2)
    canvas.create_image(PILImage.width/2, PILImage.height/2, image=photo)
    window.update()
    hue += 0.2
    if hue >= 360:
        hue = 0
