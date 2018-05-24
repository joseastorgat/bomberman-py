import os

from Utils.CC3501Utils import *
import math


####################################################
# Clase Bonus
####################################################

class Bonus(Figura):
    def __init__(self, pos=Vector(0, 0), tipo = 'speed'):
        self.tipos = {'speed':self.frutilla, 'fire': self.fuego}
        self.tipo = tipo
        self.figura = self.tipos[self.tipo]
        super().__init__(pos, (1.0, 1.0, 1.0))

    def frutilla(self):
        #Cuerpo Cabeza
        glBegin(GL_TRIANGLES)
        glColor3f(255.0/255.0, 1.0/255.0, 19.0/255.0)

        glVertex2f( 10, 35)
        glVertex2f( 25, 10)
        glVertex2f( 40, 35)
        glEnd()
        
        glBegin(GL_QUADS)
        glVertex2f( 10, 35)
        glVertex2f( 15, 45)
        glVertex2f( 35, 45)
        glVertex2f( 40, 35)
        glEnd()
        
        glBegin(GL_QUADS)
        #Ojos
        glColor3f(1.0, 1.0, 1.0)
        glVertex2f( 18, 32)
        glVertex2f( 18, 36)
        glVertex2f( 22, 36)
        glVertex2f( 22, 32)
        
        glVertex2f( 28, 32)
        glVertex2f( 28, 36)
        glVertex2f( 32, 36)
        glVertex2f( 32, 32)

        glColor3f(0.0, 0.0, 0.0)
        glVertex2f( 18, 32)
        glVertex2f( 18, 34)
        glVertex2f( 20, 34)
        glVertex2f( 20, 32)
        
        glVertex2f( 28, 32)
        glVertex2f( 28, 34)
        glVertex2f( 30, 34)
        glVertex2f( 30, 32)
        glEnd()


        #Pelo
        glBegin(GL_TRIANGLES)
        glColor3f(0.0/255.0, 255.0/255.0, 255.0/255.0)

        glVertex2f( 15, 45)
        glVertex2f( 18, 40)
        glVertex2f( 23, 45)
        

        # glVertex2f( 15, 45)
        # glVertex2f( 18, 50)
        # glVertex2f( 23, 45)
        
        glVertex2f( 21, 45)
        glVertex2f( 24, 40)
        glVertex2f( 29, 45)
        

        glVertex2f( 21, 45)
        glVertex2f( 24, 50)
        glVertex2f( 29, 45)

        glVertex2f( 27, 45)
        glVertex2f( 30, 40)
        glVertex2f( 35, 45)

        # glVertex2f( 27, 45)
        # glVertex2f( 30, 50)
        # glVertex2f( 35, 45)
        glEnd()

    def fuego(self):
        radio = 10
        paso = 20
    
        glBegin(GL_TRIANGLE_FAN)
        
        glColor3f(255.0/255.0, 1.0/255.0, 19.0/255.0)
        x=20
        y=20
        glVertex2f(x, y)
        
        for i in range(int(paso/2)-3):
            glVertex2f(x - radio*math.cos(i*2*math.pi/paso), y - radio*math.sin(i*2*math.pi/paso) )
        glEnd()


        x=30
        y=20
        glBegin(GL_TRIANGLE_FAN)

        glVertex2f(x, y)
        
        for i in range(int(paso/2)-3):
            glVertex2f(x + radio*math.cos(i*2*math.pi/paso), y - radio*math.sin(i*2*math.pi/paso) )
        glEnd()

        glBegin(GL_QUADS)
        glVertex2f(20, 20)
        glVertex2f(30, 20)
        glVertex2f(30, 10)
        glVertex2f(20, 10)

        glVertex2f(40, 20)
        glVertex2f(10, 20)
        glVertex2f(14, 35)
        glVertex2f(36, 35)
        glEnd()


        glBegin(GL_TRIANGLES)
        glVertex2f(14, 30)
        glVertex2f(18, 50)
        glVertex2f(22, 30)

        glVertex2f(22, 30)
        glVertex2f(26, 45)
        glVertex2f(30, 30)
        
        glVertex2f(30, 30)
        glVertex2f(33, 50)
        glVertex2f(36, 30)
        glEnd()


        #aMARILLO

        radio = 5
        paso = 20
    
        glBegin(GL_TRIANGLE_FAN)
        
        glColor3f(255.0/255.0, 180.0/255.0, 0./255.0)
        x=20
        y=20
        glVertex2f(x, y)
        
        for i in range(int(paso/2)-3):
            glVertex2f(x - radio*math.cos(i*2*math.pi/paso), y - radio*math.sin(i*2*math.pi/paso) )
        glEnd()


        x=30
        y=20
        glBegin(GL_TRIANGLE_FAN)

        glVertex2f(x, y)
        
        for i in range(int(paso/2)-3):
            glVertex2f(x + radio*math.cos(i*2*math.pi/paso), y - radio*math.sin(i*2*math.pi/paso) )
        glEnd()

        glBegin(GL_QUADS)
        
        glVertex2f(20, 20)
        glVertex2f(30, 20)
        glVertex2f(30, 15)
        glVertex2f(20, 15)

        glVertex2f(35, 20)
        glVertex2f(15, 20)
        glVertex2f(16, 27)
        glVertex2f(32, 27)
        glEnd()


        glBegin(GL_TRIANGLES)
        glVertex2f(15, 25)
        glVertex2f(18, 42)
        glVertex2f(21, 25)

        glVertex2f(22, 22)
        glVertex2f(26, 39)
        glVertex2f(30, 22)
        
        # glVertex2f(30, 30)
        # glVertex2f(33, 50)
        # glVertex2f(36, 30)
        glEnd()

        glColor3f(255.0/255.0, 255.0/255.0, 0./255.0)
        glBegin(GL_TRIANGLES)
        
        glVertex2f(20, 17)
        glVertex2f(20, 25)
        glVertex2f(25, 17)        
        
        glVertex2f(25, 17)
        glVertex2f(28, 23)
        glVertex2f(30, 17)        

        glEnd()