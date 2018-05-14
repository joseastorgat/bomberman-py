import os

from Utils.CC3501Utils import *
import math
import time

####################################################
# Clase Bomba
####################################################

class Bomba(Figura):
    def __init__(self, image, sound, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
        self.init_time = time.time()
        self.figura = self.Dinamita
        self.exploded = False
        self.texture = glGenTextures(1)
        self.finished = False
        self.sprites = image
        self.sound = sound
        super().__init__(pos, rgb)

    def Dinamita(self):

        #Dinamita!

        glPushMatrix()
        glTranslatef(20,-10,0)
        glRotatef(45.0,0,0,1.0)
        glBegin(GL_QUADS)

        #solido
        glColor3f(0.7, 0.0, 0.0)

        glVertex2f(8,10)
        glVertex2f(8,35)
        glVertex2f(8+10,35)
        glVertex2f(8+10,10)

        glVertex2f(20,10)
        glVertex2f(20,35)
        glVertex2f(20+10,35)
        glVertex2f(20+10,10)

        glVertex2f(33,10)
        glVertex2f(33,35)
        glVertex2f(33+10,35)
        glVertex2f(33+10,10)


        #luz
        glColor3f(1.0, 0.0, 0.0)

        glVertex2f(15,10)
        glVertex2f(15,35)
        glVertex2f(8+10,35)
        glVertex2f(8+10,10)

        glVertex2f(27,10)
        glVertex2f(27,35)
        glVertex2f(20+10,35)
        glVertex2f(20+10,10)

        glVertex2f(40,10)
        glVertex2f(40,35)
        glVertex2f(33+10,35)
        glVertex2f(33+10,10)

        #Centro
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(45,30)
        glVertex2f(45,25)
        glVertex2f(6,25)
        glVertex2f(6,30)

        glVertex2f(45,20)
        glVertex2f(45,15)
        glVertex2f(6,15)
        glVertex2f(6,20)

        #mecha*4
        glColor3f(167.0/255.0, 135.0/255.0, 0.0)

        aux = 35 + (10-int(3*(time.time() - self.init_time)))
        glVertex2f(14,35)
        glVertex2f(12,35)
        glVertex2f(12,aux)
        glVertex2f(14,aux)

        glVertex2f(26,35)
        glVertex2f(24,35)
        glVertex2f(24,aux)
        glVertex2f(26,aux)

        glVertex2f(38,35)
        glVertex2f(36,35)
        glVertex2f(36,aux)
        glVertex2f(38,aux)
        glEnd()

        #Fuego en Mecha - Rojo
        glColor3f(1.0, 0.0, 0.0)
        paso = 8
        r1 = 3

        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(13, aux);
        for i in range(paso+1):
            glVertex2f(13 + r1*math.cos(i*2*math.pi/paso), aux + r1*math.sin(i*2*math.pi/paso) )
        glEnd()

        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(25, aux);
        for i in range(paso+1):
            glVertex2f(25 + r1*math.cos(i*2*math.pi/paso), aux + r1*math.sin(i*2*math.pi/paso) )
        glEnd()
        
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(37, aux);
        for i in range(paso+1):
            glVertex2f(37 + r1*math.cos(i*2*math.pi/paso), aux + r1*math.sin(i*2*math.pi/paso) )
        glEnd()

        #Fuego en Mecha - Amarillo
        glColor3f(1.0, 1.0, 0.0)
        r2 = 1
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(13, aux);
        for i in range(paso+1):
            glVertex2f(13 + r2*math.cos(i*2*math.pi/paso), aux + r2*math.sin(i*2*math.pi/paso) )
        glEnd()        
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(25, aux);
        for i in range(paso+1):
            glVertex2f(25 + r2*math.cos(i*2*math.pi/paso), aux + r2*math.sin(i*2*math.pi/paso) )
        glEnd()
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(37, aux);
        for i in range(paso+1):
            glVertex2f(37 + r2*math.cos(i*2*math.pi/paso), aux + r2*math.sin(i*2*math.pi/paso) )
        glEnd()
        glPopMatrix()

    def Explosion(self):

        i = int((time.time() - self.init_time - 3.0)/0.1)
        if i>6:
            i=6
            self.finished=True
        
        self.load_texture(0,i)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.texture)

        x = 0
        y = 0 
        
        glBegin(GL_QUADS)

        glTexCoord(0, 0)
        glVertex(x, y, 0)
        glTexCoord(0, 1)
        glVertex(x, y + self.height, 0)
        glTexCoord(1, 1)
        glVertex(x + self.width, y + self.height, 0)
        glTexCoord(1, 0)
        glVertex(x + self.width, y, 0)

        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        
        #Derecha!
        self.load_texture(2,i)
        x = 48
        y = 0
        
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        
        glTexCoord(0, 0)
        glVertex(x, y, 0)        
        glTexCoord(0, 1)
        glVertex(x, y + self.height, 0)
        glTexCoord(1, 1)
        glVertex(x + self.width, y + self.height, 0)
        glTexCoord(1, 0)        
        glVertex(x + self.width, y, 0)
        
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)


        #Izquierda

        glBindTexture(GL_TEXTURE_2D, self.texture)        
        glBegin(GL_QUADS)
       
        x = -48
        y = 0

        glTexCoord(1, 0)
        glVertex(x, y, 0)        
        glTexCoord(1, 1)
        glVertex(x, y + self.height, 0)
        glTexCoord(0, 1)
        glVertex(x + self.width, y + self.height, 0)
        glTexCoord(0, 0)        
        glVertex(x + self.width, y, 0)

        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        

        # Arriba
        glBindTexture(GL_TEXTURE_2D, self.texture)        
        glBegin(GL_QUADS)
       
        x = 0
        y = 48

        glTexCoord(0, 0)        
        glVertex(x, y, 0)        
        glTexCoord(1, 0)
        glVertex(x, y + self.height, 0)
        glTexCoord(1, 1)
        glVertex(x + self.width, y + self.height, 0)
        glTexCoord(0, 1)
        glVertex(x + self.width, y, 0)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)


        # Abajo
        glBindTexture(GL_TEXTURE_2D, self.texture)        
        glBegin(GL_QUADS)
        x = 0
        y = -48
        glTexCoord(1, 0)
        glVertex(x, y, 0)        
        glTexCoord(0, 0)        
        glVertex(x, y + self.height, 0)
        glTexCoord(0, 1)
        glVertex(x + self.width, y + self.height, 0)
        glTexCoord(1, 1)
        glVertex(x + self.width, y, 0)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)


    def load_texture(self,j,i):
        #print("load texture {0}".format(i))
        tex = self.sprites[j][i]
        tex_surface = pygame.image.tostring(tex, 'RGBA')
        tex_width, tex_height = tex.get_size()
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_width, tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_surface)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.width = tex_width
        self.height = tex_height

    def explode(self, timeout = 3.0):
        self.crear()
        if time.time() - self.init_time> timeout:
            self.sound.play()
            self.figura = self.Explosion
            self.exploded = True
            return True
        return False
