import pygame, sys
import render
import input
import audio

from pygame.locals import *

class View:
    
    def __init__(self, eventmanager, window):
        self.event = eventmanager
        self.event.register("update", self.update)
        pygame.display.set_caption("Orpheus")
        self.render = render.Render(eventmanager, window)
        self.mix = audio.AudioManage(eventmanager)
        self.input = input.Input(eventmanager, window, self.render)
    
   
    def update(self, dt):
        
        for e in pygame.event.get():
            if e.type == QUIT:
                self.event.notify("quit")
            elif e.type == VIDEORESIZE:
                pygame.display.set_mode((e.size),pygame.RESIZABLE) 
                self.event.notify("window_resize", e.size)
            elif e.type == KEYDOWN:
                self.event.notify("key_down", e.key)
                if e.key == pygame.K_ESCAPE:
                    self.event.notify("quit")
            elif e.type == KEYUP:
                self.event.notify("key_up", e.key)
            elif e.type == MOUSEMOTION:
                self.event.notify("mouse_move", e.pos, e.rel, e.buttons)
            elif e.type == MOUSEBUTTONDOWN:
                self.event.notify("mouse_down", e.pos, e.button )
            elif e.type == MOUSEBUTTONUP:
                self.event.notify("mouse_up", e.pos, e.button)

        self.render.draw()
        self.input.draw()
        pygame.display.update()
