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
    # # Initialise screen    
    event_manager = event.EventManage()
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    event_manager.register("quit", close)


    player_view = view.View(event_manager, screen)
    game_model = model.Model(event_manager)
   # pygame.display.set_caption('Basic Pygame program')
    fpsClock = pygame.time.Clock()
    

    # # Fill background
    # background = pygame.Surface(screen.get_size())
    # background = background.convert()
    # background.fill((250, 250, 250))
    
    # # Display some text
    # font = pygame.font.Font(None, 36)
    # text = font.render("Hello There", 1, (10, 10, 10))
    # textpos = text.get_rect()
    # textpos.centerx = background.get_rect().centerx
    # background.blit(text, textpos)

    # # Blit everything to the screen
    # screen.blit(background, (0, 0))
    # pygame.display.flip()
    
    
#p1 = Planet(2,500,10)
#p2 = Planet(10,0,50)
#p1.addLink(p2,50)
#p2.addLink(p1,10)
#
#c1 = Colony(p1)
#c2 = Colony(p2)
#c1._food = 1
#print("c1: "+str(c1))
#c1.build(BuildMine())
#c1.build(BuildMine())

#for i in range(1,25):
##c1.update()
##c2.update()
##print("c1: "+str(c1))

##c1.build(BuildDrone())
#c1.build(BuildShip())

#for i in range(1,25):
##c1.update()
##c2.update()
##print("c1: "+str(c1))

#s = c1.getUnit(0)
#s.loadFood(1)
#s.go(p2)
#
#for i in range(1,25):
##c1.update()
##c2.update()
##print("c1: "+str(c1))
##print("c2: "+str(c2))

    ## Event loop (should be all the logic in this file apart from setup)
    while running:
        fpsClock.tick(settings.FRAME_TIME)
        event_manager.notify("update", fpsClock.get_time()/1000.0)
        event_manager.update()
    sys.exit()

    #event         
    #         screen.blit(background, (0, 0))
    #         pygame.display.flip()



if __name__ == '__main__': main()      
