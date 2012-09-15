import pygame, os, sys, math
import images
import menu
from pygame.locals import *
#from albow.widget import Widget
#from albow.controls import Label, Button, TextField, Column, Image
#from albow.shell import Shell, Screen, TextScreen
#from albow.grid_view import GridView
#from albow.palette_view import PaletteView
#from albow.image_array import get_image_array
#from albow.dialogs import alert, ask
#
pygame.font.init()


class Input:
    myfont = pygame.font.Font("res/fonts/8bit_nog.ttf", 20)
    myfonts = pygame.font.Font("res/fonts/8bit_nog.ttf", 16)
    builds = ["Manufactory",
              "Reclaim",
              "Fuel Extract",
              "Hydroponics"]
    units = ["Drone",
             "Transport",
            "Settler"
    ]

    def __init__(self, eventmanager, window, render):
       self.event = eventmanager
       self.window = window
       self.render = render
       self.event.register("select_planet", self.show_planet_menu)
       self.event.register("select_planet", self.show_planet_desc)          
       self.event.register("new_planet", self.add_planet)
       self.event.register("mouse_up", self.mouse_up)
       self.event.register("mouse_move", self.mouse_move)
       self.scale = 1.0
       self.offset = (0,0)
       self.planets = []
       self.over = None
       self.selected = None
       self.marker = images.marker.convert_alpha()
       self.widget = None 

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
            self.window.blit(self.planettext, self.planettextrect)
            self.widget.update()
            self.widget.draw()    

    def set_scale(self, scale):
        self.scale = scale

    def set_offset(self, offset):
        self.offset = offset
    
    def add_planet(self, planet):
        self.planets.append(PlanetButton(planet))

    def mouse_up(self,pos,button):
        if button == 1:
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
 
    #open Menu when focus given to a planet
    def show_planet_menu(self, planet):
        if not (planet == None):
            self.make_planet_menu(planet)              
            
            #self.shell = PlanetShell(self.window, planet, self.event)
            #self.shell.run() 
       
 
    def show_planet_desc(self, planet):
        if planet:
            self.planettext = Input.myfonts.render(planet.description, True, (255,255,255), (0,0,0))
            self.planettextrect = self.planettext.get_rect()
            self.planettextrect.centerx = self.window.get_rect().centerx
            self.planettextrect.centery = self.window.get_rect().centery

    def make_planet_menu(self, planet):
        self.widget = menu.Widget(0, 0, self.event, self.render)
        build_mine = menu.Menu("build mine", 150, 40, self.event, self.render, "MINE", ("build_mine", (planet)), True)
        build_menu = menu.Menu("build menu",150, 40,self.event, self.render, "BUILD", None, True)
        unit_menu = menu.Menu("unit menu", 150,40,self.event, self.render, "UNIT",None, True)
        transport_menu = menu.Menu("transport menu", 150, 40, self.event, self.render, "TRANSPORT", None, True)      
    
        for b in Input.builds:
            build_menu.add(menu.Menu(b, 150, 40, self.event, self.render, b, ("build", (planet,b))))

        for u in Input.units:
            unit_menu.add(menu.Menu(u, 150, 40, self.event, self.render, u, ("build_unit",(planet,u))))

        self.widget.add(self.widget, build_mine)
        self.widget.add(self.widget, build_menu)
        self.widget.add(self.widget, unit_menu)
        self.widget.add(self.widget, transport_menu)

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

             

#UI Shell, initialised when a planet is focussed
#class PlanetShell(Shell):

#def __init__(self, display, planet, eventmanager):
##Shell.__init__(self, display)
##self.event = eventmanager
##self.planet = planet
###create menus
##self.titletext = "Planet " + planet.name
##self.create_screens()
##self.root_screen = PlanetScreen(self, eventmanager, planet)
#   #display management
##self.set_timer(50)
##self.show_menu()
#
#def create_screens(self):
##self.build_screen = BuildScreen(self, self.event, self.planet)
##self.unit_screen = UnitScreen(self, self.event, self.planet)  
##self.transport_screen = TransportScreen(self, self.event, self.planet)  
#
#def show_menu(self):
##self.show_screen(self.root_screen)   
#
#Menu displayed when a planet is focussed
#class PlanetScreen(Screen):
 
#def __init__(self, shell, eventmanager, planet):
##Screen.__init__(self, shell.rect)
##self.shell = shell
##self.event = eventmanager
##self.planet = planet
##self.buttons = []

##def screen_button(text, screen):
###return Button(text, font = myfonts, action = lambda: shell.show_screen(screen))
#  
##buttons = [
###screen_button("Build", shell.build_screen),
###screen_button("Units", shell.unit_screen),
###Button("Colonise", font = myfonts, action = self.event.notify("colonise_planet", self.planet))
##]   
##buttons[0].enabled = not (self.planet.colony==None)
##buttons[1].enabled = not (self.planet.colony==None)##
##
##title = Label(shell.titletext)
##title.font = myfont
##menu = Column(buttons, align='l')
#
##contents = Column([
###title,
###menu,
##], align = 'l', spacing = 20)
##self.center(contents)
# 
#
#Menu displayed when adding buildings to a colonised planet
#colony_builds should contain all possible building names, associated with flags to indicate whether they are
#UNBUILT, DISABLED or ENABLED
#class BuildScreen(Screen):
#
#def __init__(self, shell, eventmanager, planet):
##Screen.__init__(self, shell.rect)
##self.shell = shell
##self.planet = planet
##self.event = eventmanager
#
##self.possbuilds = []
##self.buttons = []

   
##title = Label(shell.titletext)
##
##self.buttons.append(Button("Add Mine", font = myfonts,
#########action = self.event.notify("mine_request", self.planet.colony)));

##for b in self.possbuilds:
###self.buttons.append(Button("" + b.type, font = myfonts,
#########action = self.event.notify("building_request", self.planet.colony, b.type)))
##self.buttons.append(Button("Back",font=myfonts, action = self.back))
##title.font = myfont
##menu = Column(self.buttons, align='l')
##contents = Column([
###title,
###menu,
##], align = 'l', spacing = 20)
##self.center(contents)

#def back(self):
##self.parent.show_menu()

#Menu displayed when adding units to a colonised planet
#displays 
#class UnitScreen(Screen):
#def __init__(self, shell, planet, eventmanager):
##Screen.__init__(self, shell.rect)
##self.shell = shell
##self.planet = planet
##self.event = eventmanager
##self.buttons = []
##self.possunits = []  
#
##def screen_button(text, screen):
###return Button(text, font = myfont, action = lambda: shell.show_screen(screen))#   
##title = Label(shell.titletext)
##title.font = myfont
#  
##for u in self.possunits:
###self.buttons.append(Button("" + u.type, font = myfonts,
#########action = self.event.notify("unit_request", self.planet.colony, u.type)))
  
##self.buttons.append(Button("Back",font=myfonts, action = self.back))
#  
##menu = Column(self.buttons, align='l')
##contents = Column([
###title,
###menu,
##], align = 'l', spacing = 20)
##self.center(contents)   
# 
#def back(self):
##self.parent.show_menu()


#class TransportScreen(Screen):
#def __init__(self, shell, planet, eventmanager):
##Screen.__init__(self, shell.rect)
##self.planet = planet
##self.event = eventmanager
##self.buttons = []
##self.buttons.append(Button("Back",font=myfonts, action = self.back))
 

#def ship_ready(self, ship):
##self.event.register("select_planet", self.transport_dest_selected)

##Handles select_planet events once ship has been selected. If selected planet exists, is linked and 
##has a colony if ship is not settler
##transport is approved, this function deregistered 
#def transport_dest_selected(self, dest):
##do transportation
#
##deregister
##self.event.deregister("select_planet", self.transport_dest_selected)#


#def back(self):
##self.parent.show_menu()   



#
