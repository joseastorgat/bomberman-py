import pygame, sys
from pygame.locals import *
import time 

SCREEN_X=400
SCREEN_Y=400
#Screen size

SPRT_RECT_Y=0
SPRT_RECT_X=0

#This is where the sprite is found on the sheet

LEN_SPRT_X=48
LEN_SPRT_Y=48
#This is the length of the sprite

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y)) #Create the screen
sheet = pygame.image.load('explosion.png') #Load the sheet

sheet.set_clip(pygame.Rect(SPRT_RECT_X, SPRT_RECT_Y, LEN_SPRT_X, LEN_SPRT_Y)) #Locate the sprite you want
draw_me = sheet.subsurface(sheet.get_clip()) #Extract the sprite you want

sheet.set_clip(pygame.Rect(0, 48, LEN_SPRT_X, LEN_SPRT_Y)) #Locate the sprite you want
draw2 = sheet.subsurface(sheet.get_clip()) 
backdrop = pygame.Rect(0, 0, SCREEN_X, SCREEN_Y) #Create the whole screen so you can draw on it

screen.blit(draw_me,(0,0)) #'Blit' on the backdrop
screen.blit(draw2,(48,0)) #'Blit' on the backdrop

pygame.display.flip()

while True:
	time.sleep(10)