from OpenGL.GL import *
from Utils.CC3501Utils import *

class Vista:
    def __init__(self, fondo, ladrillos, bomber, bombas, enemigos):
        self.fondo     = fondo
        self.bomber    = bomber
        self.bombas    = bombas
        self.enemigos  = enemigos
        self.ladrillos = ladrillos

    def dibujar(self):
        # revisar si es necesario volver a negro la pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # limpiar buffers
        self.fondo.dibujar()
        
        for ladrillo in self.ladrillos:
            ladrillo.dibujar()
        
        for bomba in self.bomber.active_bombs:
            bomba.dibujar()

        for enemigo in self.enemigos:
            enemigo.dibujar()
        
        self.bomber.dibujar()
        
        pygame.display.flip()
