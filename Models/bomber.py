import os

from Utils.CC3501Utils import *
import math

from Models.bomba import Bomba

####################################################
# Clase Bomber
####################################################

class Bomber(Figura):
    _type = "bomber"

    _hero = {"cabeza":[], "torso":[], "pantalones":[], "ojos":[], "zapatos":[], "bandana":[], "piel":[]}
    _enemy = {"cabeza":[], "torso":[], "pantalones":[], "ojos":[], "zapatos":[], "bandana":[], "piel":[]}
    _burned = {"cabeza":[], "torso":[], "pantalones":[], "ojos":[], "zapatos":[], "bandana":[], "piel":[]}
    _color_scheme = {"heroe": _hero  , "enemy": _enemy}

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
        self.speed = self.speed * 1.5
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
        radio = 13

        #Cabeza
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(0, 0, 0)
        glVertex2f(25, 45);# center of circle
        for i in range(paso+1):
            glVertex2f(25 + radio*math.cos(i*2*math.pi/paso),45 + radio*math.sin(i*2*math.pi/paso) )
        glEnd()


        glBegin(GL_QUADS)
        #Cuello
        glColor3f(0.0, 0.0, 0.0)
        glVertex2f(28,40)
        glVertex2f(28,30)
        glVertex2f(22,30)
        glVertex2f(22,40)

        #Torso
        glVertex2f(30,30)
        glVertex2f(30,20)
        glVertex2f(20,20)
        glVertex2f(20,30)


        #BRAZOS
        glVertex2f(30,30)
        glVertex2f(40,20)
        glVertex2f(37,17)
        glVertex2f(30,25)

        glVertex2f(20,30)
        glVertex2f(20,25)
        glVertex2f(13,17)   
        glVertex2f(10,20)

        glColor3f(0.0, 0.0, 0.0)

        #PIERNAS

        glVertex2f(30,20)
        glVertex2f(30,15)
        glVertex2f(20,15)
        glVertex2f(20,20)

        #Pierna Izquierda
        glVertex2f(25,15)
        glVertex2f(20,10)
        glVertex2f(15,10)
        glVertex2f(20,15)

        glVertex2f(20,10)
        glVertex2f(20,5)
        glVertex2f(15,5)
        glVertex2f(15,10)

        #Pierna Derecha
        glVertex2f(25,15)
        glVertex2f(30,15)
        glVertex2f(35,10)
        glVertex2f(30,10)

        glVertex2f(35,10)
        glVertex2f(35,5)
        glVertex2f(30,5)
        glVertex2f(30,10)

        glColor3f(0.0, 0.0, 0.0)
        #Zapatos


        glVertex2f(10,0)
        glVertex2f(15,5)
        glVertex2f(20,5)
        glVertex2f(20,0)


        glVertex2f(40,0)
        glVertex2f(30,0)
        glVertex2f(30,5)
        glVertex2f(35,5)

        

        #BAndana
        
        glColor3f(1.0, 1.0, 1.0)
        

        glVertex2f(13,43)
        glVertex2f(13,47)
        glVertex2f(37,47)
        glVertex2f(37,43)



            #Ojos
        glColor3f(0.0, 0.0, 0.0)
        
        glVertex2f(18,42)
        glVertex2f(18,48)
        glVertex2f(22,48)
        glVertex2f(22,42)

        glVertex2f(28,42)
        glVertex2f(28,48)
        glVertex2f(32,48)
        glVertex2f(32,42)
        

        glEnd()




        glBegin(GL_TRIANGLES)

        glVertex2f(36,45)
        glVertex2f(40,55)
        glVertex2f(43,50)


        glVertex2f(36,45)
        glVertex2f(40,40)
        glVertex2f(43,45)

        glEnd()
