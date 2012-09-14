import pygame, os, sys, math
import images
from pygame.locals import *
from albow.widget import Widget
from albow.controls import Label, Button, TextField, Column, Image
from albow.shell import Shell, Screen, TextScreen
#from albow.grid_view import GridView
#from albow.palette_view import PaletteView
from albow.image_array import get_image_array
from albow.dialogs import alert, ask

pygame.font.init()
myfont = pygame.font.Font("8bit_nog.ttf", 20)
myfonts = pygame.font.Font("8bit_nog.ttf", 16)

class Input:
    def __init__(self, eventmanager, window, render):
       self.event = eventmanager
       self.window = window
       self.render = render
       self.event.register("select_planet", self.show_planet_menu)
       self.event.register("new_planet", self.add_planet)
       self.event.register("mouse_up", self.mouse_up)
       self.event.register("mouse_move", self.mouse_move)
       self.scale = 1.0
       self.offset = (0,0)
       self.planets = []
       self.over = None
       self.selected = None
       self.marker = images.marker.convert_alpha()
       self.context = "SPACE"

    #draw interface
    def draw(self):
        if self.over:
            x = self.over.x*self.scale + self.offset[0] - self.marker.get_width()/2
            y = self.over.y*self.scale + self.offset[1] - self.marker.get_height()/2
            self.window.blit(self.marker,(int(x),int(y)))
        if self.selected:
            x = self.selected.x*self.scale + self.offset[0] - self.marker.get_width()/2
            y = self.selected.y*self.scale + self.offset[1] - self.marker.get_height()/2
            self.window.blit(self.marker,(int(x),int(y)))

    def set_scale(self, scale):
        self.scale = scale

    def set_offset(self, offset):
        self.offset = offset
    
    def add_planet(self, planet):
        self.planets.append(PlanetButton(planet))

    def mouse_up(self,pos,button):
        if self.over:
            self.selected = self.over
            self.event.notify("select_planet", self.over.planet)
        else:
            self.selected = None
            self.event.notify("select_planet", None)

    def mouse_move(self,pos,rel,buttons):
        world_pos = ((pos[0] - self.offset[0])/self.scale, (pos[1] - self.offset[1])/self.scale)
        if self.over and not self.over.is_over(world_pos):
            self.over = None
        if not self.over:
            for p in self.planets:
                if p.is_over(world_pos):
                    self.over = p
                    return
 
    def mouse_down(self,pos,button):
        if button == 5:
            self.scale_factor *= 0.5
        if button == 4:
            self.scale_factor *= 2

    def mouse_move(self,pos,rel,buttons):
        if buttons[0]:
            self.offset = (self.offset[0]+rel[0]/self.scale_factor, self.offset[1]+rel[1]/self.scale_factor)

    #open Menu when focus given to a planet
    def show_planet_menu(self, planet):
        if not (planet == None) and self.context == "SPACE":
            self.context = "PLANET"
            self.shell = PlanetShell(self.window, planet, self.event)
            shell.run() 
        
    #close Menu when focus 
    def close_planet_menu(self):
        pass    
    
#UI Shell, initialised when a planet is focussed
class PlanetShell(Shell):

    def __init__(self, display, planet, eventmanager):
        Shell.__init__(self, display)
        self.event = eventmanager
        self.planet = planet
        #create menus
        self.titletext = "Planet " + planet.name
        self.root_screen = PlanetScreen(self, eventmanager, planet)
       #display management
        self.set_timer(50)
    
    def create_screens(self):
        self.build_screen = BuildScreen(self)
        self.unit_screen = UnitScreen(self)  
    
    def show_menu(self):
        self.show_screen(self.menu_screen)   
    
#Menu displayed when a planet is focussed
class PlanetScreen(Screen):
 
    def __init__(self, shell, eventmanager, planet):
        Screen.__init__(self, shell.rect)
        self.shell = shell
        self.event = eventmanager
        self.planet = planet
        
        def screen_button(text, screen):
            return Button(text, font = myfonts, action = lambda: shell.show_screen(screen))
                      
        title = Label(shell.titletext)
        title.font = myfont
        menu = Column([
            screen_button("Build", shell.build_screen, enable = not (self.planet.colony == None) ),
            screen_button("Units", shell.unit_screen, enable = not (self.planet.colony == None)),
            Button("Colonise", font = myfonts, action = self.event.notify("colonise_planet", self.planet))
        ], align='l')
        contents = Column([
            title,
            menu,
        ], align = 'l', spacing = 20)
        self.center(contents)
     
    
#Menu displayed when adding buildings to a colonised planet
#colony_builds should contain all possible building names, associated with flags to indicate whether they are
#UNBUILT, DISABLED or ENABLED
class BuildScreen(Screen):
    
    def __init__(self, shell, planet, eventmanager):
        Screen.__init__(self, shell.rect)
        self.shell = shell
        self.planet = planet
        self.event = eventmaanger
    
        self.possbuilds = []
        self.buttons = []

        def screen_button(text, screen):
            return Button(text, font = myfont, action = lambda: shell.show_screen(screen))       
    
        title = Label(shell.titletext)
        
        self.buttons.append(Button("Add Mine", font = myfonts,
                                    action = self.event.notify("mine_request", self.planet.colony)));

        for b in possbuilds:
            self.buttons.append(Button("" + b.type, font = myfonts,
                                    action = self.event.notify("building_request", self.planet.colony, b.type)))

        self.buttons.append(screen_button("Back", shell.menu_screen))

        title.font = myfont
        menu = Column(self.buttons, align='l')
        contents = Column([
            title,
            menu,
        ], align = 'l', spacing = 20)
        self.center(contents)

#Menu displayed when adding units to a colonised planet
#displays 
class UnitScreen(Screen):
    def __init__(self, shell, planet, eventmanager):
        self.shell = shell
        self.planet = planet
        self.event = eventmanager
        self.buttons = []
        self.possunits = []  
    
        def screen_button(text, screen):
            return Button(text, font = myfont, action = lambda: shell.show_screen(screen))       
        title = Label(shell.titletext)
        title.font = myfont

        self.buttons.append(screen_button("Back", shell.menu_screen))
        
        for u in possunits:
            self.buttons.append(Button("" + u.type, font = myfonts,
                                    action = self.event.notify("unit_request", self.planet.colony, u.type)))
      
        menu = Column(self.buttons, align='l')
        contents = Column([
            title,
            menu,
        ], align = 'l', spacing = 20)
        self.center(contents)   
      
class PlanetButton:
    earth_rad = 0.000042*500
    
    def __init__(self, planet):
        self.planet = planet
        r = math.log(planet.orbit_radius+1)
        self.x = r*math.cos(planet.orbit_phase)
        self.y = r*math.sin(planet.orbit_phase)
        
        self.r = math.log(self.earth_rad*(planet.planet_radius+0.5+0.25/planet.planet_radius)+1.01)*0.9
        self.r2 = self.r*self.r
    
    def is_over(self, pos):
        return ((self.x - pos[0])*(self.x - pos[0]) + (self.y - pos[1])*(self.y - pos[1])) < self.r2    
