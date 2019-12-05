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

mesh_chunks = 100
chunk_size = 5
mesh_size = mesh_chunks * chunk_size
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
from panda3d.core import LineSegs, NodePath, GeomVertexData, Geom, GeomVertexFormat, GeomVertexWriter, GeomTriangles, GeomNode
class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        format = GeomVertexFormat.getV3n3c4t2()
        vdata = GeomVertexData('Mesh GVD',format,Geom.UHStatic)

        gvwV = GeomVertexWriter(vdata, 'vertex')
        gvwT = GeomVertexWriter(vdata, 'texcoord')
        gvwC = GeomVertexWriter(vdata, 'color')
        gvwN = GeomVertexWriter(vdata, 'normal')

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
                # if x == 0 and y == 0:
                #     z = 10
                # print(z)
                # z = 0
                rgb = colorsys.hsv_to_rgb(z/4,0.7,0.9)
                a = 1.0
                gvwV.addData3f(x/scale,y/scale,z)
                gvwT.addData2f(x/scale,y/scale)
                gvwN.addData3f( 0.00000,0.00000, -1.00000)
                gvwC.addData4f(rgb[0],rgb[1],rgb[2],a)

                points[_y].append(ThreeDpoint(x/scale,y/scale,z))
                # print(x/scale,y/scale,z)
        print("100.0%")

        # print("Generating Lines...")
        # for y in range(mesh_size-1):
        #     print("{:.1f}%".format(100 * y / mesh_size),end="\r")
        #     for x in range(mesh_size-1):
        #         line_array.append(ThreeDline(points[y][x],points[y+1][x]))
        #         line_array.append(ThreeDline(points[y][x],points[y][x+1]))
        #         line_array.append(ThreeDline(points[y][x],points[y+1][x+1]))
        # y = mesh_size-1
        # print("{:.1f}%".format(100 * y / mesh_size),end="\r")
        # for x in range(mesh_size-1):
        #     line_array.append(ThreeDline(points[y][x],points[y][x+1]))
        # x = mesh_size-1
        # for y in range(mesh_size-1):
        #     line_array.append(ThreeDline(points[y][x],points[y+1][x]))
        # print("100.0%")
        #
        # print("Rendering Lines...")
        # line_array_len = len(line_array)
        # old_percent = -1
        # for i in range(line_array_len):
        #     percent = floor(1000 * i / line_array_len)
        #     if percent != old_percent:
        #         print("{:.1f}%".format(percent/10),end="\r")
        #         old_percent = percent
        #     pos = line_array[i]
        #     lines = LineSegs()
        #     lines.moveTo(pos.x1,pos.y1,pos.z1)
        #     lines.drawTo(pos.x2,pos.y2,pos.z2)
        #     lines.setThickness(1)
        #     node = lines.create()
        #     np = NodePath(node)
        #     np.reparentTo(self.render)
        # print("100.0%")

        f_geoms = []
        b_geoms = []
        print("Generating Mesh...")
        for c_y in range(mesh_chunks):
            print("{:.1f}%".format(100 * c_y / mesh_chunks),end="\r")
            for c_x in range(mesh_chunks):
                f_geoms.append(Geom(vdata))
                b_geoms.append(Geom(vdata))
                if c_y == mesh_chunks-1:
                    edge_y = 1
                else:
                    edge_y = 0
                if c_x == mesh_chunks-1:
                    edge_x = 1
                else:
                    edge_x = 0
                for y in range(c_y*chunk_size,((c_y+1)*chunk_size)-edge_y):
                    for x in range(c_x*chunk_size,((c_x+1)*chunk_size)-edge_x):
                        index1 = (y * mesh_size) + x
                        index2 = ((y+1) * mesh_size) + x
                        index3 = (y * mesh_size) + x+1
                        index4 = ((y+1) * mesh_size) + x+1

                        tris = GeomTriangles(Geom.UHStatic)
                        tris.addVertex(index3)
                        tris.addVertex(index2)
                        tris.addVertex(index1)
                        tris.addVertex(index2)
                        tris.addVertex(index3)
                        tris.addVertex(index4)
                        tris.closePrimitive()
                        f_geoms[(c_y*mesh_chunks)+c_x].addPrimitive(tris)

                        tris = GeomTriangles(Geom.UHStatic)
                        tris.addVertex(index1)
                        tris.addVertex(index2)
                        tris.addVertex(index3)
                        tris.addVertex(index4)
                        tris.addVertex(index3)
                        tris.addVertex(index2)
                        tris.closePrimitive()
                        b_geoms[(c_y*mesh_chunks)+c_x].addPrimitive(tris)
        print("100.0%")

        print("Rendering Mesh...")
        geoms = f_geoms + b_geoms
        for i in range(len(geoms)):
            node = GeomNode('Mesh'+str(i))
            node.addGeom(geoms[i])
            self.render.attachNewNode(node)
        print("Scene Rendered.")

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.setFrameRateMeter(True)


    def spinCameraTask(self, task):
        angleDegrees = task.time * 3.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 30)
        self.camera.setHpr(angleDegrees, -30, 0)
        return Task.cont


app = MyApp()
app.run()