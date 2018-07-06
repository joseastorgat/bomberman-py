import os
import random

import yaml
from Utils.CC3501Utils import *


from Controller.control import *

os.environ['SDL_VIDEO_CENTERED'] = '1'  # centrar pantalla

def main():
    ancho = 650
    alto = 650
    try:
	    with open("Config/config.yaml","r") as stream:
	        params = yaml.load(stream)
    
    except Exception as e:
    	print("ERROR: No se pudo cargar el archivo de configuración")
    	raise e

    game = Controller(params["win_width"],params["win_heigth"])
    run = True
    while run:
        run = game.update()
        pygame.time.wait(int(1000/30))
    pygame.quit()

main()
