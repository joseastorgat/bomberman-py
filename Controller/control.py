import pygame
import sys

#Vista
from View import vista
#Utils
from CC3501Utils import *
#Modelos
from Models.fondo    import Fondo
from Models.ladrillo import Ladrillo
from Models.bomber   import Bomber

class Controller:
    def __init__(self, width, height):


        self.fondo = Fondo()
        pos_ladrillos = borde_ladrillo(width,height)
        self.ladrillos = []
        for pos in pos_ladrillos:
            self.ladrillos.append(Ladrillo(pos))

        self.bomber = Bomber(Vector(50,50))
        self.vista = vista.Vista(self.bomber,self.fondo,self.ladrillos)
        self.run = True
    

    def update(self):

        # ver diferencia con event.get
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.bomber.move(Vector(1,0))

        elif keys[pygame.K_LEFT]:
            self.bomber.move(Vector(-1,0))

        elif keys[pygame.K_UP]:
            self.bomber.move(Vector(0,1))

        elif keys[pygame.K_DOWN]:
            self.bomber.move(Vector(0,-1))


        for event in pygame.event.get():

            if event.type == QUIT:  # cerrar ventana
                self.run = False
            if event.type == KEYDOWN:
                if event.key == K_s:
                    self.run = False

                if event.key == K_SPACE:
                    self.bomber.release_bomb()
                
                if event.key == K_p:
                    self.fondo.change_color((150/255.0, 0/255.0, 150/255.0))
        

        #Update Actual scenario

        #Action for Enemy Bombers

        self.vista.dibujar()
        pygame.display.flip()  # actualizar pantalla
        return self.run



def borde_ladrillo(width,height):

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