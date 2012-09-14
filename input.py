import os, sys
from pygame.locals import *
from albow.widget import Widget
from albow.controls import Label, Button, TextField, Column, Image
from albow.shell import Shell, Screen, TextScreen
from albow.resource import get_font, get_image
from albow.grid_view import GridView
from albow.palette_view import PaletteView
from albow.image_array import get_image_array
from albow.dialogs import alert, ask




class Input:
    font_path = "Resources/fonts/8bit_nog.ttf"

    def __init__(self, eventmanager, window, render):
       self.event = eventmanager
       self.window = window
       self.render = render
       self.event.register("planet_open", self.show_planet_menu)
       self.event.register("mouse_down", self.mouse_down) 
       self.event.register("mouse_down", self.mouse_down)
        
    #draw interface
    def draw(self):
        pass
    #draw current menu

    def mouse_down(self,pos,button):
        if button == 5:
            self.scale_factor *= 0.5
        if button == 4:
            self.scale_factor *= 2

    def mouse_move(self,pos,rel,buttons):
        if buttons[0]:
            self.offset = (self.offset[0]+rel[0]/self.scale_factor, self.offset[1]+rel[1]/self.scale_factor)

    #open Menu when focus given to a planet
    def show_planet_menu(planet_info):
        pass

    #close Menu when focus 
    def close_planet_menu
        pass    
    
#UI Shell, initialised when a planet is focussed
class PlanetShell(Shell):

    def __init__(self, display, planet_info):
        Shell.__init__(self, display)
        #create menus
        self.root_screen = PlanetScreen(self)
        self.titletext = "PLANET " + planet_name
      
        #display management
        self.set_timer(50)
    
    def create_screens(self):
        self.build_screen = BuildScreen(self)
        self.unit_screen = UnitScreen(self)  
    
    def show_menu(self):
        self.show_screen(self.menu_screen)   
    
#Menu displayed when a planet is focussed
class PlanetScreen(Screen):
    def __init__(self, shell, planet_name, colony_builds, colony_resources, colony_units):
        Screen.__init__(self, shell.rect)
        self.shell = shell
        
        myfont = pygame.font.Font("8bit_nog.ttf", 16)
        def screen_button(text, screen):
            return Button(text, font = myfont, action = lambda: shell.show_screen(screen))

        def event_button(text, buildid):
            return Button(text, font = myfont, action = None)
                
        title = Label(shell.titletext)
        title.font = myfont
        menu = Column([
            screen_button("Build", shell.build_screen),
            screen_button("Units", shell.unit_screen),
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
    def __init__(self, shell, colony_builds):
        Screen.__init__(self, shell.rect)
        self.shell = shell
        
        myfont = pygame.font.Font("8bit_nog.ttf", 16)
        def screen_button(text, screen):
            return Button(text, font = myfont, action = lambda: shell.show_screen(screen))       
        title = Label(shell.titletext)

        title.font = myfont
        menu = Column([
            screen_button("Back", shell.menu_screen)
            )
        ], align='l')
        contents = Column([
            title,
            menu,
        ], align = 'l', spacing = 20)
        self.center(contents)

#Menu displayed when adding units to a colonised planet
#displays 
class UnitScreen(Screen):
    def __init__(self, shell, colony_resources):
        self.shell = shell
        
        myfont = pygame.font.Font("8bit_nog.ttf", 16)
        def screen_button(text, screen):
            return Button(text, font = myfont, action = lambda: shell.show_screen(screen))       
        title = Label(shell.titletext)

        title.font = myfont
        menu = Column([
            screen_button("Back", shell.menu_screen)
           )
        ], align='l')
        contents = Column([
            title,
            menu,
        ], align = 'l', spacing = 20)
        self.center(contents)   

    
