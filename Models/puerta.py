import os

from Utils.CC3501Utils import *
import pygame.time as time

####################################################
# Clase Puerta
####################################################

class Puerta(Figura):
    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
        self.sombra = False
        self.init_time = 0
        self.figura = self.escondida
        super().__init__(pos, rgb)


    def set_sombra(self):
        if not self.sombra:
            self.sombra = True
            self.crear()

    def puerta(self):
        # Se dibuja la nube


        glBegin(GL_QUADS)
        glColor3f(255.0/255.0, 0.0/255.0, 0.0/255.0) #Rojo        
        glVertex2f(50,0)
        glVertex2f(0,0)
        glVertex2f(0,40)
        glVertex2f(50,40)
        glEnd()


        glPushMatrix()
        if self.init_time !=0:
            i = 1.0 - abs( time.get_ticks() - self.init_time )/2000
            glScale(i,1,1)
        else:
            i = 1

        glBegin(GL_QUADS)

        # Rectangulo principal
        glColor3f(150.0/255.0, 111.0/255.0, 51.0/255.0) #Cafe
        
        glVertex2f(25,0)
        glVertex2f(0,0)
        glVertex2f(0,40)
        glVertex2f(25,40)
        
        # Barrotes
        glColor3f(0.0/255.0, 0.0/255.0, 0.0/255.0) 

        glVertex2f(28,40)
        glVertex2f(28,0)
        glVertex2f(21,0)
        glVertex2f(21,40)

        glVertex2f(13,40)
        glVertex2f(13,0)
        glVertex2f(10,0)
        glVertex2f(10,40)
        glEnd()

        glBegin(GL_LINES)
        glColor3f(255.0/255.0, 215.0/255.0, 0.0/255.0) 

        glVertex2f(25,40)
        glVertex2f(25,0)
        glEnd()

        glPopMatrix()

        glBegin(GL_QUADS)
        glColor3f(150.0/255.0, 111.0/255.0, 51.0/255.0) #Cafe        
        
        glVertex2f(50,0)
        glVertex2f(25+(1-i)*25,0)
        glVertex2f(25+(1-i)*25,40)
        glVertex2f(50,40)
        

        glColor3f(0.0/255.0, 0.0/255.0, 0.0/255.0) 
        glVertex2f(40+(1-i)*10, 40)
        glVertex2f(40+(1-i)*10, 0)
        glVertex2f(37+(1-i)*13, 0)
        glVertex2f(37+(1-i)*13, 40)
        glEnd()


    def escondida(self):
        pass


    def abrir(self, timeout = 2.0):
        self.crear()
        
        if self.init_time == 0:
            self.init_time = time.get_ticks()

        timeout =timeout*1000
        if time.get_ticks() - self.init_time > timeout:
            return True
        return False


    def aparecer(self):
        self.figura = self.puerta

    def cerrar(self):
        self.init_time = 0
        self.crear()