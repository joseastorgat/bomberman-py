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

        radio = 10 + 4*int((time.time() - self.init_time))
        paso = 20
        x = 25
        y = 25
    
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 1.0, 1.0)
        glVertex2f(x, y);# center of circle
        for i in range(paso+1):
            glVertex2f(x + radio*math.cos(i*2*math.pi/paso),y + radio*math.sin(i*2*math.pi/paso) )
        glEnd()

    def explode(self):
        self.crear()
        return time.time() - self.init_time> 3.0

