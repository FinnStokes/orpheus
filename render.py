import pygame, os, sys, math
import images
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
        self.planet_graphics = {}
        self.background_img = images.background.convert()
        self.star_img = images.star.convert_alpha()
        self.offset = (0,0)
        self.background = None
        self._scale_background()
        self.star = None
        self.scale_dirty = True
        self.group = pygame.sprite.LayeredDirty()
    
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
            planet_rad = int(math.ceil(math.log(self.earth_rad*p.planet_radius+1)*scale))
            self.planet_graphics[p] = pygame.transform.smoothscale(self.star_img,(planet_rad*2,planet_rad*2))
    
    def add_planet(self,planet):
       self.planets.append(planet)
       self.system_radius = max(planet.orbit_radius, self.system_radius)
       self.scale_dirty = True
       w = self.window.get_width()
       h = self.window.get_height()
       PlanetSprite(planet,(w/2,h/2),self.group)
       for s in self.group.sprites():
           s.rescale(self.scale_factor*(min(w,h)*0.45)/math.log(self.system_radius+1), (w/2, h/2))
    
    def mouse_down(self,pos,button):
        if button == 5:
            self.scale_factor *= 0.5
            self.scale_dirty = True
            w = self.window.get_width()
            h = self.window.get_height()
            for s in self.group.sprites():
                s.rescale(self.scale_factor*(min(w,h)*0.45)/math.log(self.system_radius+1), pos)
        if button == 4:
            self.scale_factor *= 2
            self.scale_dirty = True
            w = self.window.get_width()
            h = self.window.get_height()
            for s in self.group.sprites():
                s.rescale(self.scale_factor*(min(w,h)*0.45)/math.log(self.system_radius+1), pos)
    
    def mouse_move(self,pos,rel,buttons):
        if buttons[0]:
            self.offset = (self.offset[0]+rel[0]/self.scale_factor, self.offset[1]+rel[1]/self.scale_factor)
            for s in self.group.sprites():
                s.move(rel)

    def draw_planet(self, planet, scale, centre):
        img = self.planet_graphics[planet]
        r = int(math.ceil(math.log(planet.orbit_radius+1)*scale))
        planet_rad = int(math.ceil(math.log(self.earth_rad*planet.planet_radius+1)*scale))
        x = int(math.ceil(centre[0] + r*math.cos(planet.orbit_phase))) - planet_rad
        y = int(math.ceil(centre[1] + r*math.sin(planet.orbit_phase))) - planet_rad
        if planet.planet_type != "dwarf planet":
            pygame.draw.circle(self.window,pygame.Color("white"),centre,r,1)
        self.window.blit(img,(x,y))
    
    def draw(self):
        if self.scale_dirty:
            self._scale_planets()
        w = self.window.get_width()
        h = self.window.get_height()
        self.group.clear(self.window,self.background)
        #self.window.blit(self.background,(0,0))
        #self.window.blit(self.background,(0,0))
        scale = self.scale_factor*(min(w,h)*0.45)/math.log(self.system_radius+1)
        centre = (int(w/2 + self.offset[0]*self.scale_factor),
                  int(h/2 + self.offset[1]*self.scale_factor))
        #pygame.draw.circle(self.window,pygame.Color("yellow"),centre,int(0.3*scale))
        if self.view == "space":
            self.group.draw(self.window)
            #self.window.blit(self.star,(centre[0]-int(self.sun_rad*scale),centre[1]-int(self.sun_rad*scale)))
            #for p in self.planets:
            #    self.draw_planet(p, scale, centre)

class PlanetSprite(pygame.sprite.DirtySprite):
    def __init__(self, planet, centre, *groups):
        pygame.sprite.DirtySprite.__init__(self, *groups)
        self.planet = planet
        self.src = images.planet.convert_alpha()
        self.image = None
        self.scale = 1
        self.offset = centre
        self.rect = self._rect()
        self.dirty = 0
    
    def _rect(self):
        r = int(math.ceil(math.log(self.planet.orbit_radius+1)*self.scale))
        planet_r = int(math.ceil(math.log(Render.earth_rad*self.planet.planet_radius+1)*self.scale))
        x = self.offset[0] + int(math.ceil(r*math.cos(self.planet.orbit_phase))) - planet_r
        y = self.offset[1] + int(math.ceil(r*math.sin(self.planet.orbit_phase))) - planet_r
        return pygame.Rect(x,y,1,1)
    
    def rescale(self, scale, mouse):
        self.offset = ((self.offset[0] - mouse[0])*scale/self.scale + mouse[0],
                       (self.offset[1] - mouse[1])*scale/self.scale + mouse[1])
        self.scale = scale
        planet_r = int(math.ceil(math.log(Render.earth_rad*self.planet.planet_radius+1)*self.scale))
        self.image = pygame.transform.smoothscale(self.src,(planet_r*2,planet_r*2))
        self.rect = self._rect()
        self.dirty = 1
    
    def move(self, diff):
        self.offset = (self.offset[0] + diff[0], self.offset[1] + diff[1])
        #self.image = None
        self.rect = self._rect()
        self.dirty = 1
    
    #def update(self):
    #    if not self.image:
    #        planet_rad = int(math.ceil(math.log(Render.earth_rad*(self.planet.planet_radius+1)*self.scale))
    #        self.image = pygame.transform.smoothscale(self.src,(planet_rad*2,planet_rad*2))
    #        self.dirty = 1
