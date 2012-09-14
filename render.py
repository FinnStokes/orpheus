import pygame, sys, math
from pygame.locals import *

class Render:
    earth_rad = 0.000042*2000
    def __init__(self, eventmanager, window):
        self.event = eventmanager
        self.event.register("new_planet", self.add_planet)
        self.event.register("mouse_down", self.mouse_down)
        self.window = window
        self.system_radius = 0
        self.scale_factor = 1
        self.view = "space"
        self.planets = []
    
    def add_planet(self,planet):
       self.planets.append(planet)
       self.system_radius = max(planet.orbit_radius, self.system_radius)
    
    def mouse_down(self,pos,button):
        if button == 5:
            self.scale_factor *= 0.5
        if button == 4:
            self.scale_factor *= 2
    
    def draw(self):
        self.window.fill(pygame.Color("black"))
        w = self.window.get_width()
        h = self.window.get_height()
        scale = self.scale_factor*(min(w,h)*0.45)/self.system_radius
        pygame.draw.circle(self.window,pygame.Color("white"),(w/2,h/2),int(0.3*scale))
        if self.view == "space":
            for p in self.planets:
                r = int(math.ceil(p.orbit_radius*scale))
                x = int(math.ceil(w/2 + r*math.cos(p.orbit_phase)))
                y = int(math.ceil(h/2 + r*math.sin(p.orbit_phase)))
                if p.planet_type != "dwarf planet":
                    pygame.draw.circle(self.window,pygame.Color("white"),(w/2,h/2),r,1)
                pygame.draw.circle(self.window,pygame.Color("white"),(x,y),int(self.earth_rad*p.planet_radius*scale))
            
