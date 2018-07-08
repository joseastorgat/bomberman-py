import os

from Utils.CC3501Utils import *
import math

from Models.bomba import Bomba
from Models.bomber import Bomber

####################################################
# Clase Bomber
####################################################

class Tortuga(Bomber):
    _type = "tortuga"

    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0), vel = Vector(0,0), speed = 5, max_bombs=1):
        super().__init__(pos, rgb, vel, speed, max_bombs)
        self.figura = self.tortuga
        self.crear()

    def tortuga(self):
        paso = 15
        radio = 20

        #Caparazon
        #colors = self._color_scheme[self.btype]

        glBegin(GL_QUADS)        
        glColor3f(0,1.0,0)

        if self.vel.x > 0 or self.vel.y>0:
            self.lado = 1
        elif self.vel.x<0 or self.vel.y<0:
            self.lado = 0


        if self.lado:        
            #Cuello
            glVertex2f(45,15)
            glVertex2f(30,15)
            glVertex2f(45,25)
            glVertex2f(55,25)

            #Cola
            glVertex2f(10,15)
            glVertex2f(10,10)
            glVertex2f(-3,10)
            glVertex2f(-6,10)
        

        else:
            #Cuello
            glVertex2f(50-45,15)
            glVertex2f(50-30,15)
            glVertex2f(50-45,25)
            glVertex2f(50-55,25)

            #Cola
            glVertex2f(50-10,15)
            glVertex2f(50-10,10)
            glVertex2f(50--3,10)
            glVertex2f(50--6,10)
        

        #Patas
        glVertex2f(8,15)
        glVertex2f(13,15)
        glVertex2f(13,3)
        glVertex2f(8,3)

        glVertex2f(18,15)
        glVertex2f(23,15)
        glVertex2f(23,3)
        glVertex2f(18,3)

        glVertex2f(28,15)
        glVertex2f(33,15)
        glVertex2f(33,3)
        glVertex2f(28,3)

        glVertex2f(37,15)
        glVertex2f(42,15)
        glVertex2f(42,3)
        glVertex2f(37,3)


        glEnd()



        #Caparazon

               
        glColor3f(165/255.0,104/255.0,42/255.0)
        
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(25, 10);# center of circle
        for i in range(paso+1):
            glVertex2f(25 + radio*math.cos(i*math.pi/paso), 10 + radio*math.sin(i*math.pi/paso))
        glEnd()

        glBegin(GL_QUADS)        
        glColor3f(0,1.0,0)
        

        if self.lado:

            #Cabeza
            glVertex2f(42,23)
            glVertex2f(60,23)
            glVertex2f(60,40)
            glVertex2f(42,40)


            #Antifaz
            glColor3f(1,0,0)
            glVertex2f(42,30)
            glVertex2f(60,30)
            glVertex2f(60,36)
            glVertex2f(42,36)
            
            #Ojo
            glColor3f(0,0,0)
            glVertex2f(54,31)
            glVertex2f(58,31)
            glVertex2f(58,35)
            glVertex2f(54,35)
            
            glEnd()

            #Boca
            glBegin(GL_LINE_STRIP)  
            glVertex2f(60,25)
            glVertex2f(58,28)
            glVertex2f(56,25)
            glVertex2f(54,28)
                  
            glEnd()


            #Antifaz2 
            glBegin(GL_TRIANGLES)
            glColor3f(1,0,0)
            glVertex2f(44,35)
            glVertex2f(36,40)
            glVertex2f(36,30)

        else:
            #Cabeza
            glVertex2f(50-42,23)
            glVertex2f(50-60,23)
            glVertex2f(50-60,40)
            glVertex2f(50-42,40)


            #Antifaz
            glColor3f(1,0,0)
            glVertex2f(50-42,30)
            glVertex2f(50-60,30)
            glVertex2f(50-60,36)
            glVertex2f(50-42,36)
            
            #Ojo
            glColor3f(0,0,0)
            glVertex2f(50-54,31)
            glVertex2f(50-58,31)
            glVertex2f(50-58,35)
            glVertex2f(50-54,35)
            
            glEnd()

            #Boca
            glBegin(GL_LINES)  
            glVertex2f(50-60,25)
            glVertex2f(50-58,28)
            glVertex2f(50-56,25)
            glVertex2f(50-54,28)
                  
            glEnd()


            #Antifaz2 
            glBegin(GL_TRIANGLES)
            glColor3f(1,0,0)
            glVertex2f(50-44,35)
            glVertex2f(50-36,40)
            glVertex2f(50-36,30)

        
        #cOLA


        glEnd()


class Humanoide(Bomber):
    _type = "humanoide"

    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0), vel = Vector(0,0), speed = 5, max_bombs=1):
        super().__init__(pos, rgb, vel, speed, max_bombs)
        self.figura = self.tortuga
        self.crear()


    def tortuga(self):

        if self.vel.x > 0:
            self.lado = 1
        elif self.vel.x<0:
            self.lado = 0


        paso = 15
        radio = 15

        #Caparazon
        #colors = self._color_scheme[self.btype]

                
        glColor3f(165/255.0,104/255.0,42/255.0)
        
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(25, 35);# center of circle
        for i in range(paso+1):
            glVertex2f(25 + radio*math.cos(i*2*math.pi/paso), 35 + radio*math.sin(i*2*math.pi/paso))
        glEnd()


        glBegin(GL_QUADS)        

        #Cuello
        glColor3f(1,1,1)

        glVertex2f(27,45)
        glVertex2f(27,30)
        glVertex2f(23,30)
        glVertex2f(23,45)


        #Cabeza
        glColor3f(0,1,0)

        #Cabeza
        glVertex2f(16,60)
        glVertex2f(34,60)
        glVertex2f(34,43)
        glVertex2f(16,43)


        #Antifaz
        glColor3f(1,0,0)
        glVertex2f(16,57)
        glVertex2f(34,57)
        glVertex2f(34,51)
        glVertex2f(16,51)
        
        #Ojos
        glColor3f(0,0,0)
        glVertex2f(18,52)
        glVertex2f(22,52)
        glVertex2f(22,56)
        glVertex2f(18,56)
        
        glVertex2f(28,52)
        glVertex2f(32,52)
        glVertex2f(32,56)
        glVertex2f(28,56)
        

        #brazo
        glColor3f(0,1,0)
        glVertex2f(38,40)
        glVertex2f(47,28)
        glVertex2f(44,25)
        glVertex2f(35,35)


        glVertex2f(50-38,40)
        glVertex2f(50-47,28)
        glVertex2f(50-44,25)
        glVertex2f(50-35,35)


        #Piernas
        glColor3f(0.0/255.0, 0.0/255.0, 0.0/255.0) 
        glVertex2f(28,20)
        glVertex2f(40,2)
        glVertex2f(34,2)
        glVertex2f(25,15)

        glVertex2f(50-28,20)
        glVertex2f(50-40,2)
        glVertex2f(50-34,2)
        glVertex2f(50-25,15)



        glEnd()


        #Boca

        glBegin(GL_LINE_STRIP)  
        glColor3f(0,0,0) 
        glVertex2f(21,45)
        glVertex2f(23,47)
        glVertex2f(25,45)
        glVertex2f(27,47)
        glVertex2f(29,45)
        glEnd()


        #Antifaz2 

        glBegin(GL_TRIANGLES)
        glColor3f(1,0,0)
        if self.lado:
            glVertex2f(18,54)
            glVertex2f(10,58)
            glVertex2f(10,52)

        else:
            glVertex2f(32,54)
            glVertex2f(40,58)
            glVertex2f(40,52)

        glEnd()


        #TORSO
        glColor3f(0,1,0)
        glBegin(GL_TRIANGLES)
        glVertex2f(25,15)
        glVertex2f(12,40)
        glVertex2f(38,40)


        glEnd()

        glBegin(GL_LINES)  
        glColor3f(0,0,0) 

        glVertex2f(25,32)
        glVertex2f(25,20)
        
        glVertex2f(20,30)
        glVertex2f(30,30)

        glVertex2f(20,26)
        glVertex2f(30,26)
        
        glVertex2f(22,22)
        glVertex2f(28,22)

        glEnd()


        glBegin(GL_TRIANGLES)

        glColor3f(0,0,0)


        glVertex2f(25,12)
        glVertex2f(30,22)
        glVertex2f(20,22)


        glEnd()