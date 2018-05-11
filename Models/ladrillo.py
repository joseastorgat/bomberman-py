import os

from Utils.CC3501Utils import *

####################################################
# Clase Ladrillo
####################################################

class Ladrillo(Figura):
    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
        self.sombra = False
        super().__init__(pos, rgb)


    def set_sombra(self):
        if not self.sombra:
            self.sombra = True
            self.crear()

    def figura(self):
        # Se dibuja la nube
        glBegin(GL_QUADS)

        # Rectangulo principal

        glColor3f(147.0/255.0, 147.0/255.0, 147.0/255.0) #Gris
        
        glVertex2f(50,0)
        glVertex2f(0,0)
        glVertex2f(0,50)
        glVertex2f(50,50)

        # Luz
        glColor3f(222.0/255.0, 222.0/255.0, 222.0/255.0) #Gris
        glVertex2f(47,47)
        glVertex2f(5,47)
        glVertex2f(0,50)
        glVertex2f(50,50)

        # Sombra
        glColor3f(102.0/255.0, 102.0/255.0, 102.0/255.0) 
        #Vertices 2n−1, 2n, 2n+2, and 2n+1 define quadrilateral n. N/2−1
        # n = 1: 1 2 4 5
        # n = 2: 3 4 6 7

        glVertex2f(50,0)
        glVertex2f(0,0)
        glVertex2f(5,5)
        glVertex2f(45,5)
        
        glVertex2f(5,5)
        glVertex2f(0,0)
        glVertex2f(0,50)
        glVertex2f(5,45)

        #Borde Derecho
        glColor3f(180.0/255.0, 180.0/255.0, 180.0/255.0) 

        glVertex2f(50,50)
        glVertex2f(50,0)
        glVertex2f(45,5)
        glVertex2f(45,45)

        if self.sombra:
            glColor3f(0.0/255.0, 72.0/255.0, 0.0/255.0) 

            glVertex2f(47, 0)
            glVertex2f(45, -3)
            glVertex2f(0, -3)
            glVertex2f(0, 0)
            glEnd()
            glBegin(GL_TRIANGLES)

            for i in range(45,3,-5):
                glVertex2i(i,-3)
                glVertex2i(i-2,-6)
                glVertex2i(i-4,-3)

        glEnd()
