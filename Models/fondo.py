import os

from Utils.CC3501Utils import *

####################################################
# Clase Fondo
####################################################

class Fondo(Figura):
    def __init__(self, pos=Vector(0, 0), rgb=(1.0, 1.0, 1.0), height=450, width=450, bgcolor = (0.0/255.0, 120.0/255.0, 0.0/255.0)):
        self.bgcolor = bgcolor
        self.width  = width
        self.height = height
        super().__init__(pos, rgb)

    def figura(self):

        glBegin(GL_QUADS)
        glColor3f(self.bgcolor[0], self.bgcolor[1], self.bgcolor[2])
        glVertex2f(self.width, 0)
        glVertex2f(0, 0)
        glVertex2f(0, self.height)
        glVertex2f(self.width, self.height)
        glEnd()

    def change_color(self, bgcolor = (103/255.0, 193/255.0, 182/255.0)):
        self.bgcolor = bgcolor
        self.lista = 0
        super().crear()
