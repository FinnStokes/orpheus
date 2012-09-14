import pygame, sys, math
from pygame.locals import *

class Render:
    earth_rad = 0.000042*2000
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
        self.offset = (0,0)
    
    def add_planet(self,planet):
       self.planets.append(planet)
       self.system_radius = max(planet.orbit_radius, self.system_radius)
    
    def mouse_down(self,pos,button):
        if button == 5:
            self.scale_factor *= 0.5
        if button == 4:
            self.scale_factor *= 2
    
    def mouse_move(self,pos,rel,buttons):
        if buttons[0]:
            self.offset = (self.offset[0]+rel[0]/self.scale_factor, self.offset[1]+rel[1]/self.scale_factor)
    
    def draw(self):
        self.window.fill(pygame.Color("black"))
        w = self.window.get_width()
        h = self.window.get_height()
        scale = self.scale_factor*(min(w,h)*0.45)/self.system_radius
        centre = (int(w/2 + self.offset[0]*self.scale_factor),
                  int(h/2 + self.offset[1]*self.scale_factor))
        pygame.draw.circle(self.window,pygame.Color("yellow"),centre,int(0.3*scale))
        if self.view == "space":
            for p in self.planets:
                r = int(math.ceil(p.orbit_radius*scale))
                x = int(math.ceil(centre[0] + r*math.cos(p.orbit_phase)))
                y = int(math.ceil(centre[1] + r*math.sin(p.orbit_phase)))
                if p.planet_type != "dwarf planet":
                    pygame.draw.circle(self.window,pygame.Color("white"),centre,r,1)
                if p.planet_type == "dwarf planet":
                    c = pygame.Color("green")
                if p.planet_type == "terrestrial planet":
                    c = pygame.Color("blue")
                if p.planet_type == "gas giant":
                    c = pygame.Color("red")
                pygame.draw.circle(self.window,c,(x,y),int(self.earth_rad*p.planet_radius*scale))
            
