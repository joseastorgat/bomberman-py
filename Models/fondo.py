import os

from CC3501Utils import *

####################################################
# Clase Fondo
####################################################

class Fondo(Figura):
    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0), bgcolor = (103.0/255.0, 193.0/255.0, 182.0/255.0)):
        self.bgcolor = bgcolor
        super().__init__(pos, rgb)

    def figura(self):

        glBegin(GL_QUADS)
        glColor3f(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2])
        glVertex2f(800, 0)
        glVertex2f(0, 0)
        glVertex2f(0, 600)
        glVertex2f(800, 600)
        glEnd()

    def change_color(self, bgcolor = (103/255.0, 193/255.0, 182/255.0)):
        self.bgcolor = bgcolor
        self.lista = 0
        super().crear()
