from OpenGL.GL import *
from CC3501Utils import *

class Vista:
    def __init__(self,bomber,fondo,ladrillos):
        self.fondo = fondo
        self.ladrillos = ladrillos
        self.bomber = bomber
    def dibujar(self):
        # revisar si es necesario volver a negro la pantalla
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # limpiar buffers
        self.fondo.dibujar()
        for ladrillo in self.ladrillos:
            ladrillo.dibujar()
        self.bomber.dibujar()
        pygame.display.flip()
