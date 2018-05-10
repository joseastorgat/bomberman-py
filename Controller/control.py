import pygame
import sys
import numpy as np
import math
#Vista
from View import vista
#Utils
from Utils.CC3501Utils import *
#Modelos
from Models.fondo    import Fondo
from Models.ladrillo import Ladrillo
from Models.bomber   import Bomber
from Models.bomba    import Bomba
from Models.bloque   import Bloque

class Controller:
    def __init__(self, width, height, scale = 50):

        """
        Condiciones Iniciales del Mundo:
            Fondo
            Bombarderos:
                Protagonista
                Enemigos x 3
            Ladrillos Indestructibles
            Ladrillos Destructibles
            Bombas:
                0

        """
        self.scale = scale

        self._w = int( math.ceil(float(width)/float(self.scale)))
        self._h = int( math.ceil(float(height)/float(self.scale)))
        
        self.fondo = Fondo()
        
        pos_ladrillos = self.get_ladrillos_pos()
        
        self.ladrillos = []
        for pos in pos_ladrillos:
            self.ladrillos.append(Ladrillo(pos))

        pos_bloques = self.get_bloques_pos()

        self.bloques = []
        for pos in pos_bloques:
            self.bloques.append(Bloque(pos))

        self.bomber = Bomber(Vector(1*scale,1*scale))
        
        self.bombas = []

        self.enemigos = [Bomber(Vector(width-2*scale, 1*scale)), 
                         Bomber(Vector(width-2*scale, height-2*scale)), 
                         Bomber(Vector(1*scale, height-2*scale))]

        self.enemigos[0].set_vel(Vector(-1,0))
        self.enemigos[1].set_vel(Vector(0,-1))
        self.enemigos[2].set_vel(Vector(1,0))

        self.explosiones  = []
        self.active_bombs = []

        self.vista = vista.Vista(self.fondo, self.ladrillos, self.bomber,  self.bombas, self.enemigos, self.bloques)

        self.run = True
    

    def update(self):
        
        self.generate_map()
        
        self.explosiones = []
        self.active_bombs = []

        # ver diferencia con event.get
        keys = pygame.key.get_pressed()

        ## Mover al bomber #####
        bomber_x = int((self.bomber.pos.x + 25)/50)
        bomber_y = int((self.bomber.pos.y + 25)/50)
        self.map[bomber_x,bomber_y] = 2

        self.bomber.set_vel(Vector(0,0))

        if keys[pygame.K_RIGHT]:
            if self.map[bomber_x + 1][bomber_y] == 0:
                self.bomber.set_vel(Vector(1,0))

        elif keys[pygame.K_LEFT]:
            if self.map[bomber_x - 1][bomber_y] == 0:
                self.bomber.set_vel(Vector(-1,0))

        elif keys[pygame.K_UP]:
            if self.map[bomber_x ][bomber_y + 1] == 0:
                self.bomber.set_vel(Vector(0,1))

        elif keys[pygame.K_DOWN]:
            if self.map[bomber_x ][bomber_y - 1] == 0:
                self.bomber.set_vel(Vector(0,-1))

        ###########################

        for event in pygame.event.get():

            if event.type == QUIT:  # cerrar ventana
                self.run = False
            if event.type == KEYDOWN:
                if event.key == K_s:
                    self.run = False

                if event.key == K_a:
                    pos_bomba = self.bomber.release_bomb()


                if event.key == K_p:
                    self.fondo.change_color((150/255.0, 0/255.0, 150/255.0))

        #Write Map!      

        #Actualizar Escenario
        # Explotar Bombas
        # Mover Enemigos

        explosion, active = self.bomber.explode_bombs()
        
        self.explosiones+=explosion
        self.active_bombs+=active
        

        self.bomber.move()

        self.move_bots()
        #Explotar Bombas
        print(self.map)

        self.vista.dibujar()

        return self.run

    def write_map(self):
        

        #pos bomber
        map[self.bomber.pos.x*self.scale][self.bomber.pos.y*scale] = "B"

        #pos bombs
        for bomb in self.bombs:
            map[bomb.x*self.scale][bomb.y*scale] = "X"

        #pos ladrillos destructibles

    def move_bots(self):

        for bot in self.enemigos:            

            bot_x = int((bot.pos.x + 25)/50)
            bot_y = int((bot.pos.y + 25)/50)

            if bot.vel.x == 0 and bot.vel.y == 0:
                des = np.random.choice(np.arange(0, 2), p=[0.2,0.8])
                
                if des == 0:
                    pass
                
                else:
                    if self.map[bot_x + 1][bot_y] == 0:
                        bot.set_vel(Vector(1, 0))

                    elif self.map[bot_x][bot_y + 1 ] == 0:
                        bot.set_vel(Vector(0, 1))

                    elif self.map[bot_x - 1][bot_y] == 0:
                        bot.set_vel(Vector(-1, 0))
                    
                    else:
                        bot.set_vel(Vector(0, -1))
            
            else:
                des = np.random.choice(np.arange(0, 4), p=[0.9,0.045,0.045,0.01])
                if des == 0 and self.map[bot_x + bot.vel.x][bot_y + bot.vel.y] == 0:
                    pass

                elif des == 1 and self.map[bot_x + bot.vel.y][bot_y + bot.vel.x] == 0:
                    bot.set_vel(Vector(bot.vel.y, bot.vel.x))

                elif des == 2 and self.map[bot_x - bot.vel.y][bot_y - bot.vel.x] == 0:
                    bot.set_vel(Vector(-bot.vel.y, -bot.vel.x))

                elif des == 3 and self.map[bot_x - bot.vel.x][bot_y - bot.vel.y] == 0:
                    bot.set_vel(Vector(-bot.vel.x, -bot.vel.y))

                else:
                    bot.set_vel(Vector(0, 0))
                
            self.map[bot_x][bot_y] = 3
            bot.move()

            bomb = np.random.choice(np.arange(0, 2), p=[0.95,0.05])
            if bomb == 1:
                bot.release_bomb()

            explosion, active = bot.explode_bombs()
            self.explosiones+=explosion
            self.active_bombs += active

    def get_ladrillos_pos(self):

        pos_ladrillos = []
        for i in range(self._h):
            pos_ladrillos.append(Vector(0,50*i))
            pos_ladrillos.append(Vector((self._w-1)*50,50*i))
        
        for i in range(self._w):
            pos_ladrillos.append(Vector(50*i, 0))
            pos_ladrillos.append(Vector(50*i, (self._h-1)*50))

        for i in range(1,self._w-1):
            for j in range(1,self._h-1):
                if i%2==0 and j%2==0:
                    pos_ladrillos.append(Vector(50*i, 50*j))

        return pos_ladrillos

    def get_bloques_pos(self):

        pos_bloques = []
        for i in range(1,self._w-1):
            for j in range(1,self._h-1):
                if i%2!=0 and j%2!=0:
                    pos_bloques.append(Vector(50*i, 50*j))
        return pos_bloques

    def generate_map(self):
        map = np.zeros((self._w, self._h))

        # Ladrillos indestructibles
        
        for ladrillo in self.ladrillos:
            map[int((ladrillo.pos.x/50)),int((ladrillo.pos.y/50)) ] = 1

        for bomb in self.active_bombs:
            map[int((bomb.x + 25)/50)][int((bomb.y + 25)/50)] = 9

        self.map = map

