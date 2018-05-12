import os

from Utils.CC3501Utils import *
import math
import time

####################################################
# Clase Bomba
####################################################

class Bomba(Figura):
    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
        self.init_time = time.time()
        super().__init__(pos, rgb)

    def figura(self):

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
        paso = 8
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


    def explode(self):
        self.crear()
        return time.time() - self.init_time> 3.0