from noise import pnoise2, snoise2

class ThreeDpoint:
    def __init__(self,x=0,y=0,z=0):
        self.set(x,y,z)
    def set(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

class ThreeDline:
    def __init__(self,p1=ThreeDpoint(),p2=ThreeDpoint()):
        self.set(p1,p2)
    def set(self,p1,p2):
        self.x1 = p1.x
        self.y1 = p1.y
        self.z1 = p1.z
        self.x2 = p2.x
        self.y2 = p2.y
        self.z2 = p2.z

mesh_size = 250
octaves = 1
scale = 2
freq = 32.0 * octaves
freq2 = 16.0 * octaves
freq3 = 8.0 * octaves


from math import pi, sin, cos, floor
import numpy
import colorsys
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import LineSegs, NodePath
class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        points = []
        line_array = []
        print("Generating Noise...")
        for _y in range(mesh_size):
            print("{:.1f}%".format(100 * _y / mesh_size),end="\r")
            y = _y - (0.5 * mesh_size)
            points.append([])
            for _x in range(mesh_size):
                x = _x - (0.5 * mesh_size)
                perlin1 = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)/128
                perlin2 = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)/128
                perlin3 = int(snoise2(x / freq, y / freq, octaves) * 127.0 + 128.0)/256
                perlin4 = int(snoise2(x / freq2, y / freq2, octaves) * 127.0 + 128.0)/256
                perlin5 = int(snoise2(x / freq3, y / freq2, octaves) * 127.0 + 128.0)/256
                z = (perlin1 * perlin2 * perlin3) + perlin4 + perlin5
                # print(z)
                # z = 0
                points[_y].append(ThreeDpoint(x/scale,y/scale,z))
                # print(x/scale,y/scale,z)
        print("100.0%")

        print("Generating Lines...")
        for y in range(mesh_size-1):
            print("{:.1f}%".format(100 * y / mesh_size),end="\r")
            for x in range(mesh_size-1):
                line_array.append(ThreeDline(points[y][x],points[y+1][x]))
                line_array.append(ThreeDline(points[y][x],points[y][x+1]))
                line_array.append(ThreeDline(points[y][x],points[y+1][x+1]))
        y = mesh_size-1
        print("{:.1f}%".format(100 * y / mesh_size),end="\r")
        for x in range(mesh_size-1):
            line_array.append(ThreeDline(points[y][x],points[y][x+1]))
        x = mesh_size-1
        for y in range(mesh_size-1):
            line_array.append(ThreeDline(points[y][x],points[y+1][x]))
        print("100.0%")

        print("Rendering Lines...")
        line_array_len = len(line_array)
        old_percent = -1
        for i in range(line_array_len):
            percent = floor(1000 * i / line_array_len)
            if percent != old_percent:
                print("{:.1f}%".format(percent/10),end="\r")
                old_percent = percent
            pos = line_array[i]
            lines = LineSegs()
            lines.moveTo(pos.x1,pos.y1,pos.z1)
            lines.drawTo(pos.x2,pos.y2,pos.z2)
            lines.setThickness(1)
            node = lines.create()
            np = NodePath(node)
            np.reparentTo(self.render)
        print("100.0%")
        print("Scene Rendered.")

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.setFrameRateMeter(True)


    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 15)
        self.camera.setHpr(angleDegrees, -25, 0)
        return Task.cont


app = MyApp()
app.run()