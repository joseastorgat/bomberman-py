import pygame
import sys
import numpy as np
import math
import random
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

        #Iniciar Pygame
        win = init(width, height, "Robots")
        
        #Iniciación de Variables a Usar:
        self.scale = scale
        self._w = int( math.ceil(float(width)/float(self.scale)))
        self._h = int( math.ceil(float(height)/float(self.scale)))
        

        self.enemigos  = []
        self.ladrillos = []
        self.bloques   = []
        self.explosiones  = []
        self.active_bombs = []


        ############################
        #   Creación de Objetos:   #
        ############################

        #Fondo <- Revisar si es necesario un fondo :s
        self.fondo = Fondo(width=width, height=height)

        #BOMBER#  - # POS INICIAL ESQ INF IZQ #

        self.bomber = Bomber(Vector(1*scale,1*scale))
        self.bomber.upgrade_max_bombs()
        
        #BLOQUES - LADRILLOS #
        pos_ladrillos = self.get_ladrillos_pos()
        for pos in pos_ladrillos:
            self.ladrillos.append(Ladrillo(pos=Vector(pos.x,pos.y)))

        pos_bloques = self.get_bloques_pos(pos_ladrillos) # <- Aleatoria
        for pos in pos_bloques:
            self.bloques.append(Bloque(pos))

        #-> ENEMIGOS <-#
        self.enemigos.append(Bomber(Vector(width-2*scale, 1*scale)))
        self.enemigos.append(Bomber(Vector(width-2*scale, height-2*scale)))
        self.enemigos.append(Bomber(Vector(1*scale, height-2*scale)))
        
        #-> POS INICIAL ENEMIGOS <-# - # ESQUINAS - TODO: Aleatoria #
        self.enemigos[0].set_vel(Vector(-1,0))
        self.enemigos[1].set_vel(Vector(0,-1))
        self.enemigos[2].set_vel(Vector(1,0))

        #Creacion mapa inicial
        self.generate_map()

        # SOMBRAS DE OBJETOS#
        for obj in self.ladrillos + self.bloques:
            if self.map[int(obj.pos.x/50)][int(obj.pos.y/50-1)] == 0:
                obj.set_sombra()

        #          Vista           #
        self.vista = vista.Vista(self.fondo, self.ladrillos, self.bomber, self.enemigos, self.bloques, self.map, win)
        self.run = True
    

    def update(self):
        
        #Generar mapa nuevamente (ver que bloques se han destruido)
        self.generate_map()

        #Obtener Teclas Apretadas
        keys = pygame.key.get_pressed()

        # Manejo de Eventos!
        for event in pygame.event.get():
            if event.type == QUIT:  # cerrar ventana
                self.run = False
            if event.type == KEYDOWN:
                if event.key == K_s:
                    self.run = False
                if event.key == K_a:
                    pos_bomba = self.bomber.release_bomb()
                    if pos_bomba:
                        self.map[int((pos_bomba.x + 25)/50)][int((pos_bomba.y + 25)/50)] = 9

        # Bombas de Bots
        self.bombs_bots()

        #Manejo de Bombas ( Explosiones y Activas )
        self.explotar_bombas()
        
        # Mover Personaje
        self.mover_personaje(keys) 
        self.bomber.move()

        # Mover BOTS
        self.move_bots()
        for bot in self.enemigos:
            bot.move()
        
        # Dibujar Todo
        self.vista.dibujar()

        return self.run


    def mover_personaje(self, keys):

        bomber_x = int((self.bomber.pos.x + 25)/50)
        bomber_y = int((self.bomber.pos.y + 25)/50)
        self.map[bomber_x,bomber_y] = 4
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

    def bombs_bots(self):
        for bot in self.enemigos:
            bomb = np.random.choice(np.arange(0, 2), p=[0.95,0.05])
            if bomb == 1:
                pos_bomba = bot.release_bomb()
                if pos_bomba:
                    self.map[int((pos_bomba.x + 25)/50)][int((pos_bomba.y + 25)/50)] = 9

    def move_bots(self):
        """
        Define movimientos aleatorios de los bots.
        
        Los bots se moverán "probabilisticamente"
            - 90% Seguir derecho
            - 4.5% Virar Derecha - Virar Izquierda
            - 1% Media Vuelta
        
        Pero si se encuentran con una pared/bomba/bloque que obstruya su paso, se quedará quieto.

        Un bot Quieto:
            - 20% Seguirá quieto
            - 80% Se moverá donde pueda moverse:
                - Derecha - Arriba - Izquierda - Abajo
        """

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

            self.map[bot_x][bot_y] = 5

    def explotar_bombas(self):
        """
        """

        #Reiniciar explosiones y bombas activas
        self.explosiones = []  # Posiciones donde una bomba acaba de explotar
        self.active_bombs = [] # Posiciones donde hay bombas activas
        rang_explosion = []

        explosion, active = self.bomber.explode_bombs()
        self.explosiones+=explosion
        self.active_bombs+=active
                
        for bot in self.enemigos:
            explosion, active = bot.explode_bombs()
            self.explosiones+=explosion
            self.active_bombs+=active

        # Explosiones!
        for bomb in self.explosiones:
            bomb_pos = (int((bomb.x+25)/50),int((bomb.y+25)/50))
            rang_explosion.append(bomb_pos)

            if self.map[bomb_pos[0]+1][bomb_pos[1]]!=1:
                rang_explosion.append((bomb_pos[0]+1,bomb_pos[1]))

            if self.map[bomb_pos[0]-1][bomb_pos[1]]!=1:
                rang_explosion.append((bomb_pos[0]-1,bomb_pos[1]))

            if self.map[bomb_pos[0]][bomb_pos[1]+1]!=1:
                rang_explosion.append((bomb_pos[0],bomb_pos[1]+1))

            if self.map[bomb_pos[0]][bomb_pos[1]-1]!=1:
                rang_explosion.append((bomb_pos[0],bomb_pos[1]-1))

        sombras = []

        #DESTRUIR BLOQUES
        for bloque in self.bloques:
            if ((bloque.pos.x)/50,(bloque.pos.y)/50) in rang_explosion:
                sombras.append(Vector((bloque.pos.x), (bloque.pos.y+50)))
                self.bloques.remove(bloque)
                del bloque
            pass
        
        # MATAR BOTS
        for bot in self.enemigos:
            if ((bot.pos.x+25)/50,(bot.pos.y+25)/50) in rang_explosion:
                self.enemigos.remove(bot)
                print("Muere BoT!")
                del bot

        # MATAR PERSONAJE -> GAME OVER
        if (int((self.bomber.pos.x+25)/50),int((self.bomber.pos.y+25)/50)) in rang_explosion:
            del self.bomber
            print("Game Over")


        # AÑADIR NUEVAS SOMBRAS GENERADAS
        for cuad in self.bloques + self.ladrillos:
            if cuad.pos in sombras:
                cuad.set_sombra()        


    def get_ladrillos_pos(self):
        """
        Entrega lista de vectores, correspondiente a la distribución incicial de ladrillos en el mapa
        """
        pos_ladrillos = []
        
        #Bordes Izquierdo y Derecho
        for i in range(self._h): 
            pos_ladrillos.append(Vector(0,50*i))
            pos_ladrillos.append(Vector((self._w-1)*50,50*i))
        
        #Bordes Superior e Inferior
        for i in range(self._w):
            pos_ladrillos.append(Vector(50*i, 0))
            pos_ladrillos.append(Vector(50*i, (self._h-1)*50))
        
        #Ladrillos indestructibles del Centro
        for i in range(1,self._w-1):
            for j in range(1,self._h-1):
                if i%2==0 and j%2==0:
                    pos_ladrillos.append(Vector(50*i, 50*j))
        
        return pos_ladrillos

    def get_bloques_pos(self,pos_ladrillos, nbloques = 4):
        """
        Entrega lista de bloques, correspondiente a la distribución incicial de bloques en el mapa
        Estas posiciones son aleatorias, sin embargo hay localizaciones donde no pueden existir estos bloques
        """

        max_bloques = int((self._h * self._w - 2*(self._h + self._w -1))/nbloques) #Numeros de bloques que se generaran
        bloques = 0
        pos_bloques = []
        pos_prohibidas = [Vector(1*50,1*50),Vector(1*50,2*50),Vector(1*50,3*50),
                        Vector((self._w-2)*50,1*50),Vector((self._w-3)*50,1*50),Vector((self._w-4)*50,1*50),
                        Vector(2*50,(self._h-2)*50),Vector(3*50,(self._h-2)*50),Vector(4*50,(self._h-2)*50),
                        Vector((self._w-2)*50,(self._h-2)*50),Vector((self._w-2)*50,(self._h-3)*50),Vector((self._w-2)*50,(self._h-4)*50)]
        
        while bloques < max_bloques:
            x = random.randint(1,self._w-2)*50
            y = random.randint(1,self._h-2)*50
            nuevo_bloque = Vector(x,y)
            if not (nuevo_bloque in pos_prohibidas or nuevo_bloque in pos_bloques or nuevo_bloque in pos_ladrillos):
                pos_bloques.append(nuevo_bloque)
                bloques+=1
        return pos_bloques

    def generate_map(self):
        self.map = np.zeros((self._w, self._h))

        # Ladrillos indestructibles
        for ladrillo in self.ladrillos:
            self.map[int((ladrillo.pos.x/50)),int((ladrillo.pos.y/50)) ] = 1

        # Bloques destructibles
        for bloque in self.bloques:
            self.map[int((bloque.pos.x/50)),int((bloque.pos.y/50)) ] = 2

        for bomb in self.active_bombs:
            self.map[int((bomb.x + 25)/50)][int((bomb.y + 25)/50)] = 9

