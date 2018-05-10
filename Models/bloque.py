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
            self.divs.append(random.randint(10,40))

        super().__init__(pos, rgb)

    def figura(self):
        # Se dibuja la nube

        glBegin(GL_QUADS)

        glColor3f(130.0/255.0, 130.0/255.0, 130.0/255.0) 

        # Rectangulo principal
        
        for i in range(0,5):

            glVertex2f(49,(i+1)*10-1)
            glVertex2f(49,i*10+1)
            glVertex2f(self.divs[i]+1,i*10+1)
            glVertex2f(self.divs[i]+1,(i+1)*10-1)

            glVertex2f(self.divs[i]-1,(i+1)*10-1)
            glVertex2f(self.divs[i]-1,i*10+1)
            glVertex2f(1,i*10+1)
            glVertex2f(1,(i+1)*10-1)
        glEnd()
