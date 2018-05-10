import os

from Utils.CC3501Utils import *
import math
import copy

from Models.bomba import Bomba

####################################################
# Clase Bomber
####################################################

class Bomber(Figura):
    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0), vel = 5.0, max_bombs=1):
        self.vel = vel
        self.max_bombs = max_bombs
        self.n_active_bombs = 0
        self.active_bombs = []
        super().__init__(pos, rgb)

    def figura(self):

        radio = 20
        paso = 20
        x = 25
        y = 25
    
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0, 0, 0)
        glVertex2f(x, y);# center of circle
        for i in range(paso+1):
            glVertex2f(x + radio*math.cos(i*2*math.pi/paso),y + radio*math.sin(i*2*math.pi/paso) )
        glEnd()


    def move(self, direction = Vector(0,1)):
        self.pos.x += self.vel * direction.x
        self.pos.y += self.vel * direction.y

    def upgrade_max_bombs(self):
        self.max_bombs+=1
        return

    def downgrade_max_bombs(self):
        self.max_bombs-=1
        return

    def release_bomb(self):
        if self.n_active_bombs < self.max_bombs:
            self.n_active_bombs+=1
            self.active_bombs.append(Bomba(pos=Vector(self.pos.x,self.pos.y)))
            print("[INFO] space pressed bomba: {0}".format(self.pos))
            return self.pos
        return None

    def explode_bombs(self):
        poses = []
        for bomb in self.active_bombs:
            if bomb.explode():
                self.n_active_bombs-=1
                poses.append(bomb.pos)
                self.active_bombs.remove(bomb)
                del bomb
        return poses