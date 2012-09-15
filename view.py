import pygame, sys, math
import render
import input
import audio

from pygame.locals import *

class View:
    myfont = pygame.font.Font("res/fonts/8bit_nog.ttf", 150)
    
    def __init__(self, eventmanager, window):
        self.event = eventmanager
        self.event.register("update", self.update)
        self.event.register("new_planet", self.new_planet)
        self.event.register("mouse_down", self.mouse_down)
        self.event.register("mouse_move", self.mouse_move)
        self.event.register("win", self.win)
        self.window = window
        pygame.display.set_caption("Orpheus")
        self.render = render.Render(eventmanager, window)
        self.mix = audio.AudioManage(eventmanager)
        self.input = input.Input(eventmanager, window, self.render)
        self.offset = (window.get_width()/2,window.get_height()/2)
        self.width = window.get_width()
        self.height = window.get_height()
        self.scale_factor = 1.0
        self.system_radius = 1.0
        self._set_scale()
        self.render.set_offset(self.offset)
        self.input.set_offset(self.offset)
        self.winScreen = False
   
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

        if self.winScreen:
            self.draw_win_screen()
        else:
            self.render.draw()
            self.input.draw()
        pygame.display.update()
    
    def win(self):
        self.winScreen = True
    
    def draw_win_screen(self):
        self.window.fill(pygame.Color("black"))
        self.render.window.blit(self.myfont.render("You Win!", 1, (255,255,255)), (75, 200, 500, 100))
    
    def _set_scale(self):
        scale = self.scale_factor*(min(self.width,self.height)*0.45)/math.log(self.system_radius+1)
        self.render.set_scale(scale)
        self.input.set_scale(scale)
    
    def new_planet(self, planet):
        if planet.orbit_radius > self.system_radius:
            self.system_radius = planet.orbit_radius
            self._set_scale()
    
    def mouse_down(self,pos,button):
        if button == 5 and self.scale_factor > 1.0:
            self.scale_factor /= 2.0**0.5
            self._set_scale()
            self.offset = ((self.offset[0] - pos[0])/2.0**0.5 + pos[0],
                           (self.offset[1] - pos[1])/2.0**0.5 + pos[1])
            self.render.set_offset(self.offset)
            self.input.set_offset(self.offset)
        if button == 4 and self.scale_factor < 32.0:
            self.scale_factor *= 2.0**0.5
            self._set_scale()
            self.offset = ((self.offset[0] - pos[0])*2.0**0.5 + pos[0],
                           (self.offset[1] - pos[1])*2.0**0.5 + pos[1])
            self.render.set_offset(self.offset)
            self.input.set_offset(self.offset)
    
    def mouse_move(self,pos,rel,buttons):
        if buttons[0]:
            self.offset = (self.offset[0]+rel[0], self.offset[1]+rel[1])
            self.render.set_offset(self.offset)
            self.input.set_offset(self.offset)
