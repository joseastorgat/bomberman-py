from OpenGL.GL import *
from OpenGL.GLUT import *
from Utils.CC3501Utils import *
import os

class Vista:
    def __init__(self, width, height, fondo, ladrillos, bomber, enemigos, bloques, bonus, puerta):
        self.fondo     = fondo
        self.bomber    = bomber
        self.enemigos  = enemigos
        self.ladrillos = ladrillos
        self.bloques   = bloques
        self.bonus     = bonus
        self.puerta    = puerta
        self.width = width
        self.height= height

    def dibujar(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # limpiar buffers
        
        self.fondo.dibujar()
        
        
        self.puerta.dibujar()
        for bonus in self.bonus:
            bonus.dibujar()

        for bomba in self.bomber.exploded_bombs:
            bomba.dibujar()

        for ladrillo in self.ladrillos:
            ladrillo.dibujar()
        
        for bloque in self.bloques:
            bloque.dibujar()

        for bomba in self.bomber.active_bombs:
            bomba.dibujar()
        
        for enemigo in self.enemigos:
            for bomba_enemiga in enemigo.active_bombs:
                bomba_enemiga.dibujar()

            for bomba in enemigo.exploded_bombs:
                bomba.dibujar()
            enemigo.crear()
            enemigo.dibujar()

        self.bomber.crear()
        
        self.bomber.dibujar()

        pygame.display.flip()


    def GameOver(self):
        self.MostrarMensaje("Game Over")


    def LevelPassed(self):
        self.MostrarMensaje("Level Complete!")


    def Level(self, level):
        self.MostrarMensaje("Level "+ str(level))



    def MostrarMensaje(self, Mensaje):
        self.dibujar()
        texture = glGenTextures(1)
        font = pygame.font.Font(os.path.join("Resources/Fonts/8bit.ttf"), 50)
        textSurface = font.render(Mensaje, True, (255,255,255,0), (0,0,0,0))
        tex_width, tex_height = textSurface.get_size()
        image = pygame.image.tostring(textSurface, "RGBX", True)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_width, tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        glPushMatrix()
        glTranslatef(int(self.width/15), int(self.height/2)-50, 0.0)
        glBindTexture(GL_TEXTURE_2D, texture)
        glBegin(GL_QUADS)
        
        x=0
        y=0
        width = self.width - 100
        height = 70
        
        glTexCoord(0, 0)
        glVertex(x, y, 0)        
        glTexCoord(0, 1)
        glVertex(x, y + height, 0)
        glTexCoord(1, 1)
        glVertex(x + width, y + height, 0)
        glTexCoord(1, 0)        
        glVertex(x + width, y, 0)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()
        
        pygame.display.flip()