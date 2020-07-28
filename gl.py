#Andree Toledo 18439
#Laboratorio 3 OBJ

import struct
from obj import Obj


def char(myChar):
		return struct.pack('=c', myChar.encode('ascii'))

def word(myChar):
	return struct.pack('=h', myChar)
	
def dword(myChar):
	return struct.pack('=l', myChar)

def normalizeColorArray(colors_array):
    return [round(i*255) for i in colors_array]

def color(r,g,b):
	return bytes([b, g, r])

BLACK = color(0,0,0)

class Render(object):
    # glInit dont needed, 'cause we have an __init__ func
    def __init__(self):
        self.framebuffer = []
        self.width = 1200
        self.height = 1200
        self.viewport_x = 0
        self.viewport_y = 0
        self.viewport_width = 1200
        self.viewport_height = 1200
        self.glClear()

    def point(self, x, y):
        self.framebuffer[y][x] = self.color

    def glCreateWindow(self, width, height):
        self.height = height
        self.width = width

    def glViewport(self, x, y, width, height):
        # Setting viewport initial values
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_height = height
        self.viewport_width = width

    def glClear(self):
        self.framebuffer = [
            [BLACK for x in range(self.width)] for y in range(self.height)
        ]

    def glClearColor(self, r=1, g=1, b=1):
        # get normalized colors as array
        normalized = normalizeColorArray([r,g,b])
        clearColor = color(normalized[0], normalized[1], normalized[2])

        self.framebuffer = [
            [clearColor for x in range(self.width)] for y in range(self.height)
        ]

    def glVertex(self, x, y):
        final_x = round((x+1) * (self.viewport_width/2) + self.viewport_x)
        final_y = round((y+1) * (self.viewport_height/2) + self.viewport_y)
        self.point(final_x, final_y)

    def glColor(self, r=0, g=0, b=0):
        # get normalized colors as array
        normalized = normalizeColorArray([r,g,b])
        self.color = color(normalized[0], normalized[1], normalized[2])

    def glCoordinate(self, value, is_vertical):
        real_coordinate = ((value+1) * (self.viewport_height/2) + self.viewport_y) if is_vertical else ((value+1) * (self.viewport_width/2) + self.viewport_x)
        return round(real_coordinate)

    def glLine(self, x0, y0, x1, y1) :
        #x0 = self.glCoordinate(x0, False)
        #x1 = self.glCoordinate(x1, False)
        #y0 = self.glCoordinate(y0, True)
        #y1 = self.glCoordinate(y1, True)

        steep = abs(y1 - y0) > abs(x1 - x0)

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0 
        y = y0
        threshold =  dx

        for x in range(x0, x1):
            self.point(y, x) if steep else self.point(x, y)
            
            offset += 2*dy

            if offset >= threshold:
                y += -1 if y0 > y1 else 1
                threshold += 2*dx

    def load(self, filename='default.obj', translate=[0,0], scale=[1,1]):
        model = Obj(filename)

        for face in model.faces:
            vcount = len(face)

            for j in range(vcount):
                vi1 = face[j][0] - 1
                vi2 = face[(j + 1) % vcount][0] - 1

                v1 = model.vertices[vi1]
                v2 = model.vertices[vi2]

                x1 = round((v1[0] * scale[0]) + translate[0])
                y1 = round((v1[1] * scale[1]) + translate[1])
                x2 = round((v2[0] * scale[0]) + translate[0])
                y2 = round((v2[1] * scale[1]) + translate[1])

                self.glLine(x1, y1, x2, y2)


    def glFinish(self, filename='output.bmp'):
        # starts creating a new bmp file
        f = open(filename, 'bw')

        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # Finishing placing points
        try:
            for x in range(self.height):
                for y in range(self.width):
                    f.write(self.framebuffer[x][y])
        except:
            print('Your obj file is too big. Try another scale/translate values')

        f.close()