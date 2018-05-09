import os
import random
from CC3501Utils import *

from Controller.control import *

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrar pantalla

def main():
    ancho = 750
    alto = 650

    init(ancho, alto, "Robots")
    game = Controller(ancho,alto)
    run = True
    while run:
        run = game.update()
        pygame.time.wait(int(1000/30))
    pygame.quit()

main()
