import os

from Utils.CC3501Utils import *
import math

from Models.bomba import Bomba

####################################################
# Clase Bomber
####################################################

class Bomber(Figura):
    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0), vel = Vector(0,0), speed = 5, max_bombs=1):
        self.max_bombs = max_bombs
        self.speed = speed
        
        self.vel = vel
        self.active_bombs = []
        self.n_active_bombs = 0
        self.exploded_bombs = []
        self.figura = self.Robot    
        super().__init__(pos, rgb)


    def move(self):
        self.pos.x += self.vel.x*self.speed 
        self.pos.y += self.vel.y*self.speed

    def set_vel(self,vel = Vector(0,1)):
        self.vel = vel

    def upgrade_speed(self):
        self.speed +=5
        print("upgrade_speed")

    def downgrade_speed(self):
        if speed ==5:
            self.speed =3
        else:
            self.speed -=5


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
                self.exploded_bombs.append(bomb) # Bomba se elimina de bombas activas
                self.active_bombs.remove(bomb) #
            else:
                active.append(bomb.pos)

        for bomb in self.exploded_bombs:
            bomb.crear()
            explode_pos = Vector(bomb.pos.x,bomb.pos.y)
            poses.append(explode_pos)

            if bomb.finished:
                self.exploded_bombs.remove(bomb)
                del bomb

        #print(poses, active)
        return poses, active


    def Robot(self):


        paso = 10
        radio = 15

        #Cabeza
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0.9, 0.9, 0.9)
        glVertex2f(25, 40);# center of circle
        for i in range(paso+1):
            glVertex2f(25 + radio*math.cos(i*2*math.pi/paso),40 + radio*math.sin(i*2*math.pi/paso) )
        glEnd()


        glBegin(GL_QUADS)

        #solido


        # #Cabeza
        # glVertex2f(15,35)
        # glVertex2f(15,55)
        # glVertex2f(35,55)
        # glVertex2f(35,35)


        #Torso
        glColor3f(1.0, 1.0, 1.0)
        glVertex2f(22,0)
        glVertex2f(22,40)
        glVertex2f(28,40)
        glVertex2f(28,0)

        #BRAZOS
        glVertex2f(10,20)
        glVertex2f(10,25)
        glVertex2f(40,25)
        glVertex2f(40,20)

        #Rueda
        glColor3f(0.0, 0.0, 0.0)

        glVertex2f(10,0)
        glVertex2f(10,10)
        glVertex2f(20,10)
        glVertex2f(20,0)

        glVertex2f(30,0)
        glVertex2f(30,10)
        glVertex2f(40,10)
        glVertex2f(40,0)

        #Ojos
        glVertex2f(18,38)
        glVertex2f(18,43)
        glVertex2f(22,43)
        glVertex2f(22,38)

        glVertex2f(28,38)
        glVertex2f(28,43)
        glVertex2f(32,43)
        glVertex2f(32,38)
        glEnd()
