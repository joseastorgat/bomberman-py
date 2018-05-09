import os

from CC3501Utils import *
import math

####################################################
# Clase Fondo
####################################################

class Bomber(Figura):
    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0), vel = 5.0, max_boms=1):
        self.vel = vel
        self.max_boms = max_boms
        self.active_boms = 0
        super().__init__(pos, rgb)

    def figura(self):

        radio = 20
        paso = 20
        x = 0
        y = 0
    
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0, 0, 0)
        glVertex2f(x, y);# center of circle
        for i in range(paso+1):
            glVertex2f(x + radio*math.cos(i*2*math.pi/paso),y + radio*math.sin(i*2*math.pi/paso) )
        glEnd()


    def move(self, direction = Vector(0,1)):
        self.pos.x += self.vel * direction.x
        self.pos.y += self.vel * direction.y

    def upgrade_bombs(self):
        self.max_boms+=1
    
    def downgrade_boms(self):
        self.max_boms-=1

    def release_boms(self):
        if self.active_boms < self.max_boms:
            return self.pos