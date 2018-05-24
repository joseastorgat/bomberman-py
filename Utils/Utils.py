import os
import pygame


def get_explosion_sprites():
    spr_len=48
    sheet = pygame.image.load(os.path.join('Resources/explosion/explosion.png')) #Load the sheet
    sprites = []
    for i in range(0,3):
        subsprite = []
        for j in range(0,7):
            sheet.set_clip(pygame.Rect(spr_len*j,spr_len*i, spr_len, spr_len)) #Locate the sprite you want
            subsprite.append(sheet.subsurface(sheet.get_clip())) #Extract the sprite you want
        sprites.append(subsprite)    
    return sprites

def get_explosion_sounds():
    sound = pygame.mixer.Sound(os.path.join("Resources/explosion/explosion.ogg"))
    sound.set_volume(1.0)
    return sound

