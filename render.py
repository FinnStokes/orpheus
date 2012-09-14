import pygame, os, sys, math
import images
import random
from pygame.locals import *

class Render:
    earth_rad = 0.000042*500
    sun_rad = 0.4
    def __init__(self, eventmanager, window):
        self.event = eventmanager
        self.event.register("new_planet", self.add_planet)
        self.event.register("mouse_down", self.mouse_down)
        self.event.register("mouse_move", self.mouse_move)
        self.window = window
        self.system_radius = 0
        self.scale_factor = 1.0
        self.view = "space"
        self.planets = []
        self.planet_img = {}
        self.planet_graphics = {}
        self.background_img = images.background.convert()
        self.star_img = images.star.convert_alpha()
        self.offset = (self.window.get_width()/2,self.window.get_height()/2)
        self.background = None
        self._scale_background()
        self.star = None
        self.scale_dirty = True
    
    def _scale_background(self):
        w = self.window.get_width()
        h = self.window.get_height()
        bgw = self.background_img.get_width()
        bgh = self.background_img.get_height()
        bgscale = max(w*1.0/bgw, h*1.0/bgh)
        bgw = int(math.ceil(bgw*bgscale))
        bgh = int(math.ceil(bgh*bgscale))
        self.background = pygame.transform.smoothscale(self.background_img,(bgw,bgh)).subsurface(pygame.Rect(0,0,w,h))
    
    def _scale_planets(self):
        w = self.window.get_width()
        h = self.window.get_height()
        if self.system_radius > 0:
            scale = self.scale_factor*(min(w,h)*0.45)/math.log(self.system_radius+1)
        else:
            scale = self.scale_factor
        self.star = pygame.transform.smoothscale(self.star_img,(int(self.sun_rad*2*scale),int(self.sun_rad*2*scale)))
        for p in self.planets:
            r = int(math.ceil(math.log(p.orbit_radius+1)*scale))
            planet_r = int(math.ceil(math.log(self.earth_rad*p.planet_radius+1.01)*scale*0.9))
            self.planet_graphics[p] = pygame.transform.smoothscale(self.planet_img[p],(planet_r*2,planet_r*2))
    
    def add_planet(self,planet):
       self.planets.append(planet)
       self.system_radius = max(planet.orbit_radius, self.system_radius)
       if planet.planet_type == "dwarf planet":
           imgs = [images.asteroid]
       if planet.planet_type == "terrestrial planet":
           imgs = [images.planet]
       if planet.planet_type == "gas giant":
           imgs = [images.orange_gas_giant, images.blue_gas_giant]
       self.planet_img[planet] = random.choice(imgs).convert_alpha()
       self.scale_dirty = True
    
    def mouse_down(self,pos,button):
        if button == 5 and self.scale_factor > 1.0:
            self.scale_factor /= 2.0
            self.offset = ((self.offset[0] - pos[0])/2.0 + pos[0],
                           (self.offset[1] - pos[1])/2.0 + pos[1])
            self.scale_dirty = True
        if button == 4 and self.scale_factor < 32.0:
            self.scale_factor *= 2.0
            self.offset = ((self.offset[0] - pos[0])*2.0 + pos[0],
                           (self.offset[1] - pos[1])*2.0 + pos[1])
            self.scale_dirty = True
    
    def mouse_move(self,pos,rel,buttons):
        if buttons[0]:
            self.offset = (self.offset[0]+rel[0], self.offset[1]+rel[1])

    def draw_planet(self, planet, scale, centre):
        img = self.planet_graphics[planet]
        r = int(math.ceil(math.log(planet.orbit_radius+1)*scale))
        planet_r = int(math.ceil(math.log(self.earth_rad*planet.planet_radius+1.01)*scale*0.9))
        x = int(math.ceil(centre[0] + r*math.cos(planet.orbit_phase))) - planet_r
        y = int(math.ceil(centre[1] + r*math.sin(planet.orbit_phase))) - planet_r
        if planet.planet_type != "dwarf planet":
            pygame.draw.circle(self.window,pygame.Color("white"),centre,r,1)
        self.window.blit(img,(x,y))
    
    def draw(self):
        if self.scale_dirty:
            self._scale_planets()
            self.scale_dirty = False
        w = self.window.get_width()
        h = self.window.get_height()
        self.window.blit(self.background,(0,0))
        scale = self.scale_factor*(min(w,h)*0.45)/math.log(self.system_radius+1)
        centre = (int(self.offset[0]),
                  int(self.offset[1]))
        if self.view == "space":
            self.window.blit(self.star,(centre[0]-int(self.sun_rad*scale),centre[1]-int(self.sun_rad*scale)))
            for p in self.planets:
                self.draw_planet(p, scale, centre)
