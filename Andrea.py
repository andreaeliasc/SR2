#Andrea Elias
#Graficas
import struct

#Estructura de tamanio caracter
def char(c):
    return struct.pack('=c', c.encode('ascii'))
#Estructura de tamanio word
def word(c):
    return struct.pack('=h', c)
#Estructura de tamanio dword
def dword(c):
    return struct.pack('=l', c)
#Asignar un color RGB
def color(r, g, b):
    return bytes([b, g, r])

#Objeto Bitmap para controlar renderizado
class Bitmap(object):
    def __init__(self):
        self.framebuffer = []

    def glpoint(self, x, y):
        self.framebuffer[y][x] = self.color

    def glInit(self):
        pass

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height

    def glViewport(self, x, y, width, height):
        self.xViewPort = x
        self.yViewPort = y
        self.viewPortWidth = width
        self.viewPortHeight = height

    def glClear(self):
        self.framebuffer = [
            [color(0, 0, 0) for x in range(self.width)]
            for y in range(self.height)
        ]

    def glClearColor(self, r=1, g=1, b=1):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)

        self.framebuffer = [
            [color(r, g, b) for x in range(self.width)]
            for y in range(self.height)
        ]

    def glColor(self, r=0.5, g=0.5, b=0.5):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
        self.color = color(r, g, b)

    def glCordX(self, x):
        return round((x+1)*(self.viewPortWidth/2)+self.xViewPort)

    def glCordY(self, y):
        return round((y+1)*(self.viewPortHeight/2)+self.yViewPort)

    def glVertex(self, x, y):
        X = self.glCordX(x)
        Y = self.glCordY(y)
        self.point(X, Y)

    def glPoint(self, x, y):
        X = self.glCordX(x)
        Y = self.glCordY(y)
        self.point(X, Y)


    def glLine(self, x0, y0, x1, y1):
        x0 = self.glCordX(x0)
        y0 = self.glCordY(y0)
        x1 = self.glCordX(x1)
        y1 = self.glCordY(y1)

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0 
        threshold =  dx
        y = y0
        inc = 1 if y1 > y0 else -1
        for x in range(x0, x1):
            if steep:
                self.glpoint(y, x)
            else:
                self.glpoint(x, y)

            offset += 2 * dy
            if offset >= threshold:
                y += inc
                threshold += 2 * dx

#Genera la imagen renderizada en formato bmp recibiendo el nombre de la imagen como imagen.bmp
    def glFinish(self, filename='Panda.bmp'):
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

        # pixel data
        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[y][x])

        f.close()


objeto = Bitmap()

objeto.glCreateWindow(100,100)
objeto.glClearColor(0,0,0)
objeto.glViewport(25,25,50,50)
objeto.glColor(0,0,0)
objeto.glColor(0,1,1)
objeto.glLine(-1,-1,1,1)
objeto.glFinish()
