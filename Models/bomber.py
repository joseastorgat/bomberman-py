import os

from Utils.CC3501Utils import *
import math
import copy

from Models.bomba import Bomba

####################################################
# Clase Bomber
####################################################

class Bomber(Figura):
    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0), vel = Vector(0,0), rapidez = 5, max_bombs=1):
        self.max_bombs = max_bombs
        self.rapidez = rapidez
        
        self.vel = vel
        self.active_bombs = []
        self.n_active_bombs = 0
        self.exploded_bombs = []
        
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


    def move(self):
        self.pos.x += self.vel.x*self.rapidez 
        self.pos.y += self.vel.y*self.rapidez

    def set_vel(self,vel = Vector(0,1)):
        self.vel = vel

    def upgrade_max_bombs(self):
        self.max_bombs+=1
        return

    def downgrade_max_bombs(self):
        self.max_bombs-=1
        return

    def release_bomb(self, image ,sound):
        if self.n_active_bombs < self.max_bombs:
            self.n_active_bombs+=1
            self.active_bombs.append(Bomba(image=image, pos=Vector(int((self.pos.x+25)/50)*50,int((self.pos.y+25)/50)*50),sound=sound))
            print("[INFO] space pressed bomba: {0}".format(self.pos))
            return self.pos
        return None

    def explode_bombs(self):
        poses = []
        active = []
        for bomb in self.active_bombs:

            if bomb.explode():
                self.n_active_bombs-=1
                explode_pos = Vector(bomb.pos.x,bomb.pos.y)
                poses.append(explode_pos)
                self.exploded_bombs.append(bomb) # Bomba se elimina de bombas activas
                self.active_bombs.remove(bomb) #
            else:
                active.append(bomb.pos)

        for bomb in self.exploded_bombs:
            bomb.crear()
            if bomb.finished:
                self.exploded_bombs.remove(bomb)
                del bomb

        #print(poses, active)
        return poses, active

