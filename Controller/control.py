import pygame
import sys
import numpy as np

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
        #self.map = generate_initial_map(width,height,scale)

        self.fondo = Fondo()
        
        pos_ladrillos = get_ladrillos_pos(width,height)
        
        self.ladrillos = []
        for pos in pos_ladrillos:
            self.ladrillos.append(Ladrillo(pos))

        pos_bloques = get_bloques_pos(width,height)

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

        self.vista = vista.Vista(self.fondo, self.ladrillos, self.bomber,  self.bombas, self.enemigos, self.bloques)
        self.run = True
    

    def update(self):

        # ver diferencia con event.get
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.bomber.set_vel(Vector(1,0))

        elif keys[pygame.K_LEFT]:
            self.bomber.set_vel(Vector(-1,0))

        elif keys[pygame.K_UP]:
            self.bomber.set_vel(Vector(0,1))

        elif keys[pygame.K_DOWN]:
            self.bomber.set_vel(Vector(0,-1))

        else:
            self.bomber.set_vel(Vector(0,0))

        for event in pygame.event.get():

            if event.type == QUIT:  # cerrar ventana
                self.run = False
            if event.type == KEYDOWN:
                if event.key == K_s:
                    self.run = False

                if event.key == K_SPACE:
                    pos_bomba = self.bomber.release_bomb()
                    # if pos_bomba:
                    #     bomba = Bomba(pos =Vector(pos_bomba.x, pos_bomba.y))
                    #     print("[INFO] space pressed bomba: {0}".format(pos_bomba))
                    #     self.bombas.append(bomba)

                if event.key == K_p:
                    self.fondo.change_color((150/255.0, 0/255.0, 150/255.0))
        

        #Update Actual scenario
        self.bomber.explode_bombs()
        self.bomber.move()

        for enemigo in self.enemigos:
            
            des = np.random.choice(np.arange(0, 4), p=[0.8,0.075,0.075,0.05])
            if des == 0:
                pass
            
            elif des == 1:
                enemigo.set_vel(Vector(enemigo.vel.y, enemigo.vel.x))

            elif des == 2:
                enemigo.set_vel(Vector(-enemigo.vel.y, -enemigo.vel.x))

            elif des == 4:
                enemigo.set_vel(Vector(-enemigo.vel.x, -enemigo.vel.y))

            enemigo.move()

            bomb = np.random.choice(np.arange(0, 2), p=[0.95,0.05])
            if bomb == 1:
                enemigo.release_bomb()
            enemigo.explode_bombs()


        #Action for Enemy Bombers
        self.vista.dibujar()
        pygame.display.flip()  # actualizar pantalla
        return self.run

        def write_map(self):
            

            #pos bomber
            map[self.bomber.pos.x*self.scale][self.bomber.pos.y*scale] = "B"

            #pos bombs
            for bomb in self.bombs:
                map[bomb.pos.x*self.scale][bomb.pos.y*scale] = "X"

            #pos ladrillos destructibles


def get_ladrillos_pos(width,height):

    pos_ladrillos = []
    for i in range(int(height/50)):
        pos_ladrillos.append(Vector(0,50*i))
        pos_ladrillos.append(Vector(width-50,50*i))
    
    for i in range(int(width/50)):
        pos_ladrillos.append(Vector(50*i, 0))
        pos_ladrillos.append(Vector(50*i, height-50))

    for i in range(1,int(width/50)-1):
        for j in range(1,int(height/50)-1):
            if i%2==0 and j%2==0:
                pos_ladrillos.append(Vector(50*i, 50*j))

    return pos_ladrillos

def get_bloques_pos(width,height):

    pos_bloques = []

    for i in range(1,int(width/50)-1):
        for j in range(1,int(height/50)-1):
            if i%2!=0 and j%2!=0:
                pos_bloques.append(Vector(50*i, 50*j))
    return pos_bloques




def generate_initial_map(width,height,scale):
    _width  = int(width/scale)
    _height = int(height/scale)
    
    map = np.zeros(_width, _height)

    # Ladrillos indestructibles
    for i in range(int(height/scale)):
        map[0][i] = "I"
        map[_width-1][i] = "I"
    
    for i in range(int(width/scale)):
        map[i][0] = "I"
        map[i][_height-1] = "I"

    for i in range(1,int(width/scale)-1):
        for j in range(1,int(height/scale)-1):
            if i%2==0 and j%2==0:
                map[i][j] = "I"
    return map

