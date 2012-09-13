import os, sys
import pygame
from pygame.locals import *
import event
import view
import model
import settings

from planet import *
from colony import *

#if not pygame.font: print('Warning, fonts disabled')
#if not pygame.mixer: print('Warning, sound disabled')
running = True

def close():
    global running 
    running = False
         
def main():
    # # Initialise screen and event manager  
    event_manager = event.EventManage()
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    event_manager.register("quit", close)

    #initialise view, model
    player_view = view.View(event_manager, screen)
    game_model = model.Model(event_manager)
    fpsClock = pygame.time.Clock()
    

    ## Event loop (should be all the logic in this file apart from setup)
    while running:
        fpsClock.tick(settings.FRAME_TIME)
        event_manager.notify("update", fpsClock.get_time()/1000.0)
        event_manager.update()

if __name__ == '__main__': main()      
