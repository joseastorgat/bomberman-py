from OpenGL.GL import *
from Utils.CC3501Utils import *

class Vista:
    def __init__(self, fondo, ladrillos, bomber, bombas, enemigos, bloques):
        self.fondo     = fondo
        self.bomber    = bomber
        self.bombas    = bombas
        self.enemigos  = enemigos
        self.ladrillos = ladrillos
        self.bloques   = bloques

    def dibujar(self):
        # revisar si es necesario volver a negro la pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # limpiar buffers
        self.fondo.dibujar()
        
        for ladrillo in self.ladrillos:
            ladrillo.dibujar()
        
        for bloque in self.bloques:
            bloque.dibujar()

        for enemigo in self.enemigos:
            for bomba_enemiga in enemigo.active_bombs:
                bomba_enemiga.dibujar()
        
            enemigo.dibujar()
        
        self.bomber.dibujar()
        
        for bomba in self.bomber.active_bombs:
            bomba.dibujar()
        
        pygame.display.flip()
