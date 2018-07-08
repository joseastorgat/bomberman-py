import pygame
import sys
import numpy as np
import math
import random
import os
import yaml
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
from Models.bomber    import Ninja
from Models.ladrillo  import Ladrillo
from Models.puerta    import Puerta
from Models.tortuga   import Tortuga
from Models.tortuga   import Humanoide

# from Models.salida    import Salida




class Controller:
    def __init__(self, width, height, scale = 50, level = 0, multiplayer=False):

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


        try:
            with open("Config/lvl"+str(level%4)+".yaml","r") as stream:
                self.params = yaml.load(stream)
    
        except Exception as e:
            print("ERROR: No se pudo cargar el archivo de configuración del nivel ")
            raise e

        self.width = self.params["win_width"]
        self.height = self.params["win_height"]
        

        self.level=level
        win = init(self.width, self.height, "Ninja!")
        
        #Iniciación de Variables a Usar:
        self.scale = scale
        self._w = int( math.ceil(float(self.width)/float(self.scale)))
        self._h = int( math.ceil(float(self.height)/float(self.scale)))
        
        self.run = True
        self.game_over = False
        self.level_passed = False


        self.enemigos  = []
        self.ladrillos = []
        self.bloques   = []
        self.active_bombs = []
        
        ############################################
        #      FONDO - BLOQUES INDESTRUCTIBLES     #
        ############################################

        #FONDO
        self.fondo = Fondo(width=self.width, height=self.height, bgcolor = self.params["floor_color"])
        
        #LADRILLOS
        pos_ladrillos = self.create_ladrillos()

        #######################################
        #####        PERSONAJES           #####
        #######################################    
        
        # -> BOMBER <-#  
        bomber_pos = Vector(self.params["bomber_initial_pose"][0]*scale,self.params["bomber_initial_pose"][1]*scale)
        self.bomber = Bomber(bomber_pos, speed= self.params["bomber_initial_speed"], max_bombs=self.params["bomber_initial_bombs"] )#, btype="heroe")

        #-> ENEMIGOS <-#
        self.enemigos = []
        self.bots_can_bomb = self.params["bots_can_bomb"]

        pos_prohibidas = pos_ladrillos + [bomber_pos]#+ enemy_pos
        enemys_pos = self.create_enemys(enemy_type='bomber', n1=self.params["n_ninjas"], n2=self.params["n_tortuga"], n3=self.params["n_tortuga_humanoide"], pos_prohibidas=pos_prohibidas)

        

        #############################
        #   BLOQUES DESTRUCTIBLES   #
        #############################
        
        pos_bloques = self.create_bloques(pos_prohibidas=pos_prohibidas, nbloques=self.params["n_bloques"]) # <- Aleatoria
                
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
        self.create_bonus(pos_bloques, self.params["n_bonus"])


        #######################################
        #####       Vista                 #####
        #######################################    
        self.vista = vista.Vista(self.width, self.height, self.fondo, self.ladrillos, self.bomber, self.enemigos, self.bloques, self.bonus, self.puerta)
        self.vista.dibujar()
        self.vista.Level(level)
        pygame.time.wait(500)
        #Musica y Sprites#
        #Obtención de Sprites de Explosiones

        #######################################
        ####           RESOURCES          #####
        #######################################
        self.sprites = get_explosion_sprites()
        self.bomb_sound = get_explosion_sounds()
        files = os.listdir("Resources/theme")
        pygame.mixer.music.load("Resources/theme/"+files[random.randint(0, len(files)-1)])
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.6)

        #Game Over Music and SOur
        go_files = os.listdir("Resources/GameOver")    
        self.go_sound = pygame.mixer.Sound("Resources/GameOver/"+go_files[random.randint(0, len(go_files)-1)])


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
        if self.bots_can_bomb:
            self.bombs_bots()

        #Manejo de Bombas (Explosiones y Activas)
        self.explotar_bombas()

        # Mover BOTS
        self.move_bots()
        
        # Mover Personajes
        self.mover_personaje(keys) 


        # Asignar y Borrar Bonus
        self.manage_bonus()
        self.update_puerta()
        # Dibujar Todo
        self.vista.dibujar()
        

        if self.game_over:
            pygame.time.wait(250)
            pygame.mixer.music.pause()
            pygame.time.wait(250)
            self.go_sound.play()
            pygame.time.wait(500)
            self.vista.GameOver()
            pygame.time.wait(4000)
            self.__init__(self.width, self.height)
        
        elif self.level_passed:
            pygame.time.wait(250)
            # pygame.mixer.music.pause()
            self.go_sound.play()
            pygame.time.wait(500)
            self.vista.LevelPassed()
            pygame.time.wait(4000)
            self.__init__(self.width, self.height, level=self.level+1)
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

        if abs(self.bomber.pos.x - self.puerta.pos.x)<20 and abs(self.bomber.pos.y - self.puerta.pos.y)<20:
            if self.puerta.abrir():
                self.level_passed = True
        else:
            self.puerta.cerrar()


    def explotar_bombas(self):
        """
        """
        #Reiniciar explosiones y bombas activas
        explosiones = []  # Posiciones donde una bomba acaba de explotar
        self.active_bombs = [] # Posiciones donde hay bombas activas
        
        rang_explosion = []
        rang_explosion_player = []

        explosion, active = self.bomber.explode_bombs()
        explosiones_player = explosion
        explosiones += explosion
        self.active_bombs+=active

        for bot in self.enemigos:
            explosion, active = bot.explode_bombs()
            explosiones+=explosion
            self.active_bombs+=active

        # Explosiones!
        for bomb in explosiones:
            bomb_pos = (int((bomb.x+25)/50),int((bomb.y+25)/50))
            rang_explosion.append(bomb_pos)

            rang_explosion.append((bomb_pos[0]+1,bomb_pos[1]))
            rang_explosion.append((bomb_pos[0]-1,bomb_pos[1]))
            rang_explosion.append((bomb_pos[0],bomb_pos[1]+1))
            rang_explosion.append((bomb_pos[0],bomb_pos[1]-1))

        for bomb in explosiones_player:
            bomb_pos = (int((bomb.x+25)/50),int((bomb.y+25)/50))
            rang_explosion_player.append(bomb_pos)
            rang_explosion_player.append((bomb_pos[0]+1,bomb_pos[1]))
            rang_explosion_player.append((bomb_pos[0]-1,bomb_pos[1]))
            rang_explosion_player.append((bomb_pos[0],bomb_pos[1]+1))
            rang_explosion_player.append((bomb_pos[0],bomb_pos[1]-1))


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
            if (int((bot.pos.x+25)/50),int((bot.pos.y+25)/50)) in rang_explosion_player:
                self.enemigos.remove(bot)
                print("Muere BoT!")
                del bot

        # MATAR PERSONAJE -> GAME OVER
        if (int((self.bomber.pos.x+25)/50),int((self.bomber.pos.y+25)/50)) in rang_explosion:
            #del self.bomber
            self.bomber.burn()
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

            bot_x = int((bot.pos.x +25)/50)
            bot_y = int((bot.pos.y +25)/50)

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

        for bot in self.enemigos:
            bot.move()

    def bombs_bots(self):
        for bot in self.enemigos:
            bomb = np.random.choice(np.arange(0, 2), p=[0.975,0.025])
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
        self.bomber.set_vel(Vector(0,0))

        self.map[bomber_x, bomber_y] = 4

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

        for enemy in self.enemigos:
            if abs(enemy.pos.x - self.bomber.pos.x)<20 and abs(enemy.pos.y - self.bomber.pos.y)<20:
                self.game_over = True

        self.bomber.move()
        

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

    def create_bloques(self, nbloques = 4, pos_prohibidas = [] ):
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
                self.bloques.append(Bloque(nuevo_bloque))
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
    

    def create_bonus(self,  pos_bloques, nbonus=4):
        """
        Create bonus
        """
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


    def create_enemys(self, enemy_type, n1, n2, n3, pos_prohibidas=[]):
        enemys_pos = []
        for i in range(0,n1):
            ninja, ninja_pos = self.create_enemy(pos_prohibidas, "ninja") 
            self.enemigos.append(ninja)
            enemys_pos.append(ninja_pos)

        for i in range(0,n2):
            tortuga, tortuga_pos = self.create_enemy(pos_prohibidas, "tortuga") 
            self.enemigos.append(tortuga)
            enemys_pos.append(tortuga_pos)

        for i in range(0,n3):
            tortuga, tortuga_pos = self.create_enemy(pos_prohibidas, "tortuga_humanoide") 
            self.enemigos.append(tortuga)
            enemys_pos.append(tortuga_pos)

        return enemys_pos


    def create_enemy(self, pos_prohibidas, E):

        Enemy_dic = {"ninja":Ninja, "tortuga": Tortuga, "tortuga_humanoide": Humanoide}
        Enemy = Enemy_dic[E]
        while True:
            x = random.randint(1,self._w-2)*50
            y = random.randint(1,self._h-2)*50
            enemy_pos = Vector(x,y)
            if not ( enemy_pos in pos_prohibidas):
                enemy = Enemy(enemy_pos, speed=self.params["enemy_"+E+"_speed"], max_bombs = self.params["enemy_"+E+"_bombs"])
                break
        return enemy, enemy_pos