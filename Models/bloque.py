import os
import random
from Utils.CC3501Utils import *

####################################################
# Clase Bloque
####################################################

class Bloque(Figura):
    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0)):
        self.divs = []
        for i in range(0,5):
            self.divs.append(random.randint(5,45))
        self.sombra = False
        super().__init__(pos, rgb)

    def set_sombra(self):
        if not self.sombra:
            self.sombra = True
            self.crear()

    def figura(self):
        # Se dibuja la nube

        glBegin(GL_QUADS)

        glColor3f(130.0/255.0, 130.0/255.0, 130.0/255.0) 

        # Rectangulo principal
        
        for i in range(0,5):
            glVertex2f(50,(i+1)*10-1)
            glVertex2f(50,i*10+1)
            glVertex2f(self.divs[i]+1,i*10+1)
            glVertex2f(self.divs[i]+1,(i+1)*10-1)

            glVertex2f(self.divs[i]-1,(i+1)*10-1)
            glVertex2f(self.divs[i]-1,i*10+1)
            glVertex2f(0,i*10+1)
            glVertex2f(0,(i+1)*10-1)
        
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