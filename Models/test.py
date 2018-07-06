import pygame
from pygame.locals import *
from OpenGL.GL import *
import sys

class Sprite(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0 
        self.texture = glGenTextures(1)

    def load_texture(self, texture_url):
        tex = pygame.image.load(texture_url)
        tex_surface = pygame.image.tostring(tex, 'RGBA')
        tex_width, tex_height = tex.get_size()
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_width, tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_surface)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.width = tex_width
        self.height = tex_height

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def render(self):
        #glColor(1, 1, 1, 1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex(self.x, self.y, 0)
        glTexCoord(0, 1)
        glVertex(self.x, self.y + self.height, 0)
        glTexCoord(1, 1)
        glVertex(self.x + self.width, self.y + self.height, 0)
        glTexCoord(1, 0)
        glVertex(self.x + self.width, self.y, 0)
        glEnd()
        glBindTexture(GL_TEXTURE_2D, 0)

def init_gl():
    window_size = width, height = (550, 400)
    pygame.init()
    pygame.display.set_mode(window_size, OPENGL | DOUBLEBUF)
    glEnable(GL_TEXTURE_2D)
    glMatrixMode(GL_PROJECTION)
    glOrtho(0, width, height, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

if __name__ == "__main__":
    init_gl()
    tile1 = Sprite()
    tile1.load_texture("explosion.png")
    tile1.set_position(50, 100)
    tile2 = Sprite()
    tile2.load_texture("explosion.png")
    tile2.set_position(80, 130)
    tiles = [tile1, tile2]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        glClear(GL_COLOR_BUFFER_BIT)
        glColor(1, 0, 0, 1)
        for tile in tiles:
            tile.render()
        pygame.display.flip()