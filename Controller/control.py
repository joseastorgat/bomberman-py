import pygame
import sys
import numpy as np
import math
import random
import os
#wait
from View import vista

#Utils
from Utils.CC3501Utils import *
from Utils.Utils import *

#Modelos
from Models.bonus     import Bonus
from Models.fondo     import Fondo
from Models.bomba     import Bomba
from Models.bloque    import Bloque
from Models.bomber    import Bomber
from Models.ladrillo  import Ladrillo
from Models.puerta    import Puerta

# from Models.salida    import Salida




class Controller:
    def __init__(self, width, height, scale = 50, nenemigos=3, multiplayer=False):

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
        self.game_over = False

        #Iniciar Pygame
        self.width = width
        self.height = height
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
        #self.bombas_explotadas = []


        ############################################
        #      FONDO - BLOQUES INDESTRUCTIBLES     #
        ############################################

        #FONDO
        self.fondo = Fondo(width=width, height=height)


        #LADRILLOS
        pos_ladrillos = self.create_ladrillos()



        #######################################
        #####        PERSONAJES           #####
        #######################################    
        
        # -> BOMBER <-#  
        self.bomber = Bomber(Vector(1*scale,1*scale))

        #-> ENEMIGOS <-#
        self.enemigos = []
        enemys_pos = self.create_enemys(enemy_type='bomber', n=0, pos_prohibidas=pos_ladrillos)
        
        

        #############################
        #   BLOQUES DESTRUCTIBLES   #
        #############################
        pos_prohibidas = pos_ladrillos #+ enemy_pos
        pos_bloques = self.get_bloques_pos(pos_prohibidas=pos_prohibidas) # <- Aleatoria
        for pos in pos_bloques:
            self.bloques.append(Bloque(pos))

        
        j = random.randint(1, len(pos_bloques)-1)
        self.puerta = Puerta(pos_bloques[j])



        #MAPA
        self.generate_map()

        # SOMBRAS DE OBJETOS#
        for obj in self.ladrillos + self.bloques:
            if self.map[int(obj.pos.x/50)][int(obj.pos.y/50-1)] == 0:
                obj.set_sombra()


        #######################################
        #####        BONUS                #####
        #######################################    
        self.bonus = []
        self.set_bonus(pos_bloques, 4)


        #######################################
        #####       Vista                 #####
        #######################################    
        self.vista = vista.Vista(self.fondo, self.ladrillos, self.bomber, self.enemigos, self.bloques, self.bonus, self.puerta)
        
        #Musica y Sprites#
        #Obtención de Sprites de Explosiones
        self.sprites = get_explosion_sprites()
        self.bomb_sound = get_explosion_sounds()

        pygame.mixer.music.load("Resources/maintheme.mp3")
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.25)
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
                    pos_bomba = self.bomber.release_bomb(self.sprites,self.bomb_sound)
                    if pos_bomba:
                        self.map[int((pos_bomba.x + 25)/50)][int((pos_bomba.y + 25)/50)] = 9

        # Colocar Bombas de Bots
        self.bombs_bots()

        #Manejo de Bombas (Explosiones y Activas)
        self.explotar_bombas()
        
        # Mover Personajes
        self.mover_personaje(keys) 
        self.bomber.move()

        # Mover BOTS
        self.move_bots()
        for bot in self.enemigos:
            bot.move()

        # Asignar y Borrar Bonus
        self.manage_bonus()
        self.update_puerta()

        # Dibujar Todo
        self.vista.dibujar()
        if self.game_over:
            pygame.time.wait(2000)
            self.vista.GameOver()
            pygame.time.wait(4000)
            #self.run=False
            self.__init__(self.width, self.height)
        return self.run



    #Update Mundo

    def manage_bonus(self):
        bombers = [self.bomber] + self.enemigos
        for bomber in bombers:
            for bonus in self.bonus:
                if abs(bonus.pos.x - bomber.pos.x)<20 and abs(bonus.pos.y - bomber.pos.y)<20:
                    if bonus.tipo == 'speed':
                        bomber.upgrade_speed() 
                    elif bonus.tipo == 'fire':
                        bomber.upgrade_max_bombs()
                    self.bonus.remove(bonus)
                    del bonus
                else:
                    continue

    def update_puerta(self):

        if abs(self.bomber.pos.x - self.puerta.pos.x)<10 and abs(self.bomber.pos.y - self.puerta.pos.y)<10:
            if self.puerta.abrir():
                self.game_over = True
        else:
            self.puerta.cerrar()


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
            #self.bombas_explotadas.append(Explosion(image= self.sprites, pos=Vector(bomb.x, bomb.y)))
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
            #del self.bomber
            print("Game Over")
            self.game_over = True

        # AÑADIR NUEVAS SOMBRAS GENERADAS
        for cuad in self.bloques + self.ladrillos:
            if cuad.pos in sombras:
                cuad.set_sombra()        


    #Movimiento de Bots
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
                

                #mov_des = (((bot.pos.x + 25)%50 <35)  and ((bot.pos.x + 25)%50 > 15 )) and (((bot.pos.y + 25)%50 <35)  and ((bot.pos.y + 25)%50 > 15 ))
                mov_des =False
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

    def bombs_bots(self):
        for bot in self.enemigos:
            bomb = np.random.choice(np.arange(0, 2), p=[0.95,0.05])
            if bomb == 1:
                pos_bomba = bot.release_bomb(self.sprites,self.bomb_sound)
                if pos_bomba:
                    self.map[int((pos_bomba.x + 25)/50)][int((pos_bomba.y + 25)/50)] = 9

    ###########################
    #Movimiento de Personajes #
    ###########################

    def mover_personaje(self, keys):
        bomber_x = int((self.bomber.pos.x + 25)/50)
        bomber_y = int((self.bomber.pos.y + 25)/50)
        self.map[bomber_x,bomber_y] = 4
        self.bomber.set_vel(Vector(0,0))

        if keys[pygame.K_RIGHT]:
            if self.map[bomber_x + 1][bomber_y] == 0 or (self.bomber.pos.x + 25)%50 < 35:
                self.bomber.set_vel(Vector(1,0))

        elif keys[pygame.K_LEFT]:
            if self.map[bomber_x - 1][bomber_y] == 0 or (self.bomber.pos.x + 25)%50 > 15:
                self.bomber.set_vel(Vector(-1,0))

        elif keys[pygame.K_UP]:
            if self.map[bomber_x ][bomber_y + 1] == 0 or (self.bomber.pos.y + 25)%50 < 35:
                self.bomber.set_vel(Vector(0,1))

        elif keys[pygame.K_DOWN]:
            if self.map[bomber_x ][bomber_y - 1] == 0 or (self.bomber.pos.y + 25)%50 > 15:
                self.bomber.set_vel(Vector(0,-1))

    

    ###########################
    #    Creación del Mundo   #
    ###########################

    def create_ladrillos(self):
        """
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

        for pos in pos_ladrillos:
            self.ladrillos.append(Ladrillo(pos=pos))
        
        return pos_ladrillos

    def get_bloques_pos(self, nbloques = 4, pos_prohibidas = [] ):
        """
        Entrega lista de bloques, correspondiente a la distribución incicial de bloques en el mapa
        Estas posiciones son aleatorias, sin embargo hay localizaciones donde no pueden existir estos bloques
        """

        max_bloques = int((self._h * self._w - 2*(self._h + self._w -1))/nbloques) #Numeros de bloques que se generaran
        bloques = 0
        pos_bloques = []
        
        pos_prohibidas += [Vector(1*50,1*50),Vector(1*50,2*50),Vector(1*50,3*50)]
        
        while bloques < max_bloques:
            x = random.randint(1,self._w-2)*50
            y = random.randint(1,self._h-2)*50
            nuevo_bloque = Vector(x,y)
            if not (nuevo_bloque in pos_prohibidas + pos_bloques):
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
    

    def set_bonus(self,  pos_bloques, nbonus=4):
        bonus_pos = []
        nladrillos = len(pos_bloques)
        i=0
        while i<nbonus:
            j = random.randint(1, nladrillos-1)
            pos = Vector(pos_bloques[j].x,  pos_bloques[j].y)
            if not pos in bonus_pos:
                i+=1
                bonus_pos.append(pos)

        for pos in bonus_pos:
            tipo = random.randint(0,1)
            tipo = 'fire' if tipo==1 else 'speed'
            self.bonus.append(Bonus(pos, tipo))


    def create_enemys(self, enemy_type, n, pos_prohibidas=[]):
        
        enemys_type = {'bomber':Bomber, 'ninja':'', 'ghost':''}
        enemys_pos = []
        enemy = 0

        while enemy < n:
            x = random.randint(1,self._w-2)*50
            y = random.randint(1,self._h-2)*50
            enemy_pos = Vector(x,y)
            
            if not ( enemy_pos in pos_prohibidas):
                enemys_pos.append(enemy_pos)
                self.enemigos.append(Bomber(enemy_pos))
                enemy+=1
            
        return enemys_pos
