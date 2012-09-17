import pygame, os, sys, math
import images
import menu
import buildings
import units
from pygame.locals import *

#Settings
PADDING = 10
MENU_WIDTH = 150
SUBMENU_WIDTH = 200
RESOURCE_BOX_WIDTH = 100
RESOURCE_BOX_LINE_HEIGHT = 15

#pygame.font.init()

class Input:
    typeStyleTitle = pygame.font.Font("res/fonts/8bit_nog.ttf", 20)
    typeStyleComment = pygame.font.Font(None, 20)
    builds = ["Factory",
              "Reclaim",
              "Fuel Extract",
              "Hydroponics"]
    
    build_comments = {"Hydroponics":"",
                      "Factory": "2 metal",
                      "Reclamation":"1 metal",
                      "FuelExtractor":""                     

    }
    unit_comments = { "Orpheus":"20 metal, 1k fuel, 1k food",
                      "Drone": "1 metal",  
                      "Transport": "expends fuel",
                      "Settler": "expends fuel"   }
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
        self.event.register("new_turn", self.new_turn)
        self.event.register("resourceupdate", self.update_resources)
        self.event.register("unit_built", self.unit_built)
        self.event.register("unit_destroyed", self.unit_destroyed)
        self.event.register("unit_moved", self.unit_moved)
        self.event.register("select_unit", self.select_unit)
        self.scale = 1.0
        self.offset = (0,0)
        self.planets = []
        self.over = None
        self.selected = None
        self.marker = images.marker.convert_alpha()
        self.widget = None 

        #end turn button
        self.endturnbtn = pygame.Rect(10,10,150,40)
        self.endturnbtn.bottomleft = self.window.get_rect().bottomleft
        self.endturnbtn.left += PADDING
        self.endturnbtn.top += -PADDING

        #turn counter
        self.turn = 1
        self.turncounter = self.typeStyleTitle.render("Turn 1", 1, (255,255,255), )
        self.turncounterrect = self.turncounter.get_rect()
        self.turncounterrect.centerx = self.window.get_rect().centerx
        self.turncounterrect.top = self.window.get_rect().top
        self.turncounterrect.top += PADDING

        #Resources
        self.resourceTitle = self.typeStyleTitle.render("RAW", 1, (255,255,255), (0,0,0))
        self.harvestedResourceTitle = self.typeStyleTitle.render("HARVESTED", 1, (255,255,255), (0,0,0))

        self.resourceTitleRect = self.resourceTitle.get_rect();
        self.harvestedResourceTitleRect = self.harvestedResourceTitle.get_rect();
        
        self.resourceTitleRect.width = RESOURCE_BOX_WIDTH
        self.harvestedResourceTitleRect.width = RESOURCE_BOX_WIDTH

        self.selected_unit = None
        self.load_menu = None

    #draw interface
    def draw(self):
        if self.over:
            x = self.over.x*self.scale + self.offset[0] - self.marker.get_width()/2
            y = self.over.y*self.scale + self.offset[1] - self.marker.get_height()/2
            self.window.blit(self.marker,(int(x),int(y)))
            if self.selected_unit:
                cost = self.selected_unit._colony.costTo(self.over.planet)
                self.render.window.blit(self.typeStyleTitle.render(str(cost*self.selected_unit.fuelFactor), 1, (255,255,255),(0,0,0)), (int(x) + self.marker.get_width() + 10, int(y) + self.marker.get_height()/2 - 10))
        if self.selected:
            x = self.selected.x*self.scale + self.offset[0] - self.marker.get_width()/2
            y = self.selected.y*self.scale + self.offset[1] - self.marker.get_height()/2
            self.window.blit(self.marker,(int(x),int(y)))
            self.planettext.render(self.window)
            self.window.blit(self.planetname, self.planetnamerect)
            if self.widget:
                self.widget.update()
                self.widget.draw()
            
            self.resourceTitleRect.width = RESOURCE_BOX_WIDTH
            
            rect = self.resourceTitleRect.copy()
            self.window.blit(self.resourceTitle, rect)
            
            rect.top += RESOURCE_BOX_LINE_HEIGHT + 10
            self.window.blit(self.resourceMetal, rect)

            rect.top += RESOURCE_BOX_LINE_HEIGHT
            self.window.blit(self.resourceFuel, rect)

            rect.top += RESOURCE_BOX_LINE_HEIGHT
            self.window.blit(self.resourceFood, rect)

            if self.harvestedResourceTitle:
              self.harvestedResourceTitleRect.width = RESOURCE_BOX_WIDTH
              rect = self.harvestedResourceTitleRect.copy()
              
              self.window.blit(self.harvestedResourceTitle, rect)
              
              rect.top += RESOURCE_BOX_LINE_HEIGHT + 10
              self.window.blit(self.harvestedResourceMetal, rect)

              rect.top += RESOURCE_BOX_LINE_HEIGHT
              self.window.blit(self.harvestedResourceFuel, rect)

              rect.top += RESOURCE_BOX_LINE_HEIGHT
              self.window.blit(self.harvestedResourceFood, rect)
              
        self.window.blit(self.turncounter, self.turncounterrect)
        
        #Draw end turn button
        pygame.draw.rect(self.window, (255,255,255), self.endturnbtn)
        
        #Offset the text a little
        textOffset = pygame.Rect(self.endturnbtn.left+10, self.endturnbtn.top+10, self.endturnbtn.width, self.endturnbtn.height)
        
        #Draw text on End turn button
        self.render.window.blit(self.typeStyleTitle.render("End Turn", 1, (0,0,0)), textOffset)

    def new_turn(self):
       self.turn += 1
       self.turncounter = self.typeStyleTitle.render("Turn "+str(self.turn), 1, (255,255,255), (0,0,0))
       self.turncounterrect = self.turncounter.get_rect()
       self.turncounterrect.top = self.window.get_rect().top
       self.turncounterrect.centerx = self.window.get_rect().centerx
       
       if self.selected_unit == None and self.load_menu:
            self.transport_menu.remove(self.load_menu)
            self.load_menu = None

    def set_scale(self, scale):
        self.scale = scale

    def set_offset(self, offset):
        self.offset = offset
    
    def add_planet(self, planet):
        self.planets.append(PlanetButton(planet))

    def mouse_up(self,pos,button):
        if button == 1 and not(self.selected and self.widget and self.widget.rect().collidepoint(pos)):
            if self.endturnbtn.collidepoint(pos):
                self.event.notify("new_turn")
            elif self.over:
                if self.selected_unit:
                    self.selected_unit.go(self.over.planet)
                    self.selected_unit = None
                else:
                    self.selected = self.over
                    self.event.notify("select_planet", self.over.planet)
            else:
                if self.selected_unit:
                    self.selected_unit = None
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
        if not (planet == None) and planet.colony:
            self.make_planet_menu(planet)
            
            #self.shell = PlanetShell(self.window, planet, self.event)
            #self.shell.run() 
       
 
    def show_planet_desc(self, planet):

        if planet:
            window_rect = self.window.get_rect()
            self.planettext = TextField(planet.description, Input.typeStyleComment, 300)
            self.planettext.rect.top = 30
            self.planettext.rect.right = window_rect.right
            self.planetname = Input.typeStyleTitle.render(planet.name, True, (255,255,255), (0,0,0))
            self.planetnamerect = self.planetname.get_rect()
            self.planetnamerect.bottomleft = self.planettext.rect.topleft
            
            self.resourceTitle = self.typeStyleTitle.render("RAW", 1, (255,255,255), (0,0,0))
            self.resourceMetal = self.typeStyleComment.render("Metal: " + str(planet.metal), 1, (255,255,255), (0,0,0))
            self.resourceFuel = self.typeStyleComment.render( "Fuel:  " + str(planet.fuel), 1, (255,255,255), (0,0,0))
            self.resourceFood = self.typeStyleComment.render( "Food:  " + str(planet.food), 1, (255,255,255), (0,0,0))
            
            self.resourceTitleRect = self.resourceTitle.get_rect();
            self.resourceTitleRect.bottomright = self.window.get_rect().bottomright;
            self.resourceTitleRect.left += -PADDING - ((RESOURCE_BOX_WIDTH + PADDING) * 2)
            self.resourceTitleRect.top += -PADDING - (RESOURCE_BOX_LINE_HEIGHT*4)

            if planet.colony:
                #hresources
                self.harvestedResourceTitle = self.typeStyleTitle.render("HARVESTED", 1, (255,255,255), (0,0,0))
                self.harvestedResourceMetal = self.typeStyleComment.render("Metal: " + str(planet.colony.metal), 1, (255,255,255), (0,0,0))
                self.harvestedResourceFuel = self.typeStyleComment.render( "Fuel:  " + str(planet.colony.fuel), 1, (255,255,255), (0,0,0))
                self.harvestedResourceFood = self.typeStyleComment.render( "Food:  " + str(planet.colony.food), 1, (255,255,255), (0,0,0))
                self.harvestedResourceTitleRect = self.harvestedResourceTitle.get_rect();
                self.harvestedResourceTitleRect.bottomright = self.window.get_rect().bottomright;
                self.harvestedResourceTitleRect.left += -PADDING - PADDING
                self.harvestedResourceTitleRect.top += -PADDING - (RESOURCE_BOX_LINE_HEIGHT*4)
            else:
                self.harvestedResourceTitle = None

    def update_resources(self,planet,resourceid,amount):
        if self.selected and self.selected.planet == planet:
            self.resources = self.typeStyleTitle.render("Raw: Metal = "+str(planet.metal)+", Fuel = "+str(planet.fuel)+", Food = "+str(planet.food), 1, (255,255,255), (0,0,0))
            self.resourcesrect = self.resources.get_rect()
            self.resourcesrect.bottomright = self.window.get_rect().bottomright
            if planet.colony:
                self.hresources = self.typeStyleTitle.render("Harvested: Metal = "+str(planet.colony.metal)+", Fuel = "+str(planet.colony.fuel)+", Food = "+str(planet.colony.food), 1, (255,255,255), (0,0,0))
                self.hresourcesrect = self.hresources.get_rect()
                self.hresourcesrect.bottomright = self.window.get_rect().bottomright
                self.resourcesrect.bottomright = self.hresourcesrect.topright
            else:
                self.hresources = None
            

    def make_planet_menu(self, planet):
        screen_width, screen_height = self.window.get_size()

        self.widget = menu.Widget(PADDING, PADDING, self.event, self.render)
        self.widget.setrect(MENU_WIDTH, screen_height-40)
        build_mine = menu.Menu("build mine", MENU_WIDTH, 40, self.event, self.render, "MINE", ("build_mine", (planet,),), True)
        build_menu = menu.Menu("build menu",MENU_WIDTH, 40,self.event, self.render, "BUILD", None, True)
        unit_menu = menu.Menu("unit menu", MENU_WIDTH, 40,self.event, self.render, "UNIT",None, True)

        self.transport_menu = menu.Menu("transport menu", MENU_WIDTH, 40, self.event, self.render, "TRANSPORT", None, True)      
   
         
        childColor = pygame.Color("grey")
        
        for b in buildings.buildings():
            title = b[1].name
            comment = Input.build_comments[str(b[0])]
            newmenu = menu.Menu(str(b[0]), SUBMENU_WIDTH, 40, self.event, self.render, title, ("build", (planet, b[1])),comment=comment)
            newmenu.colour = childColor;
            newmenu.originalColour = childColor;
            build_menu.add(newmenu)

        for u in units.units():
            title = str(u[1].name) #str(u[0])[:6]
            comment = Input.unit_comments[str(u[0])]
            newmenu = menu.Menu(str(u[0]), SUBMENU_WIDTH, 40, self.event, self.render, title, ("build_unit",(planet, u[1])), comment=comment)
            newmenu.colour = childColor;
            newmenu.originalColour = childColor;
            unit_menu.add(newmenu)

        for u in planet.colony.units():
            newmenu = menu.Menu(u, SUBMENU_WIDTH, 40, self.event, self.render, u.name, ("select_unit", (u,)))
            newmenu.colour = childColor;
            newmenu.originalColour = childColor;
            self.transport_menu.add(newmenu)

        self.widget.add(self.widget, build_mine)
        self.widget.add(self.widget, build_menu)
        self.widget.add(self.widget, unit_menu)
        self.widget.add(self.widget, self.transport_menu)
        
    def unit_built(self, planet, unit):
        if self.selected and self.selected.planet == planet and self.transport_menu:
            self.ship_select_menu = menu.Menu(unit, 150, 40, self.event, self.render, unit.name, ("select_unit", (unit,)))
            self.transport_menu.add(self.ship_select_menu)
    
    def unit_destroyed(self, unit):
        if unit in self.selected.planet.colony.units():
            rem = None
            for m in self.transport_menu.children:
                if m.id == unit:
                    rem = m
                    break
            self.transport_menu.remove(m)
    
    def unit_moved(self, unit, to):
        if self.selected and self.selected.planet == to and self.transport_menu: 
            self.transport_menu.add(menu.Menu(unit, 150, 40, self.event, self.render, unit.name, ("select_unit", (unit,))))
        elif unit in self.selected.planet.colony.units():
            rem = None
            for m in self.transport_menu.children:
                if m.id == unit:
                    rem = m
                    break
            self.transport_menu.remove(m)
    
    def select_unit(self, unit):
        self.selected_unit = unit

        self.load_menu = menu.Menu("load menu", 150, 40, self.event, self.render, "LOAD", None, visible = True)

        loadmetal = menu.Menu("load metal", 150, 40, self.event, self.render, "METAL", ("load", (unit, "Metal", 100)))
        loadfuel = menu.Menu("load fuel", 150, 40, self.event, self.render, "FUEL", ("load", (unit, "Fuel", 100)))
        loadfood = menu.Menu("load food", 150, 40, self.event, self.render, "FOOD", ("load", (unit, "Food", 100)))
        loaddrone = menu.Menu("load drones", 150, 40, self.event, self.render, "DRONE", ("load_unit",(unit, "Drone")))
        self.load_menu.add(loadmetal)
        self.load_menu.add(loadfuel)
        self.load_menu.add(loadfood)
        self.load_menu.add(loaddrone)

        self.transport_menu.add(self.load_menu)


class TextField:
    def __init__(self, text, font, width, antialias=True, foreground=(255,255,255), background=(0,0,0)):
        words = text.split(" ")
        line = ""
        self.lines = []
        self.rect = pygame.Rect(0,0,width,0)
        for word in words:
            new_line = line + word + " "
            (w, h) = font.size(new_line)
            if w > width:
                rect = pygame.Rect(0,self.rect.height,w,h)
                self.rect.height += h
                self.lines.append((font.render(line, antialias, foreground, background),rect))
                line = word + " "
            else:
                line = new_line
        rect = pygame.Rect(0,self.rect.height,w,h)
        self.rect.height += h
        self.lines.append((font.render(line, antialias, foreground, background),rect))
        
    def render(self,window):
        for line in self.lines:
            rect = line[1]
            window.blit(line[0], pygame.Rect(rect.x + self.rect.left, rect.y + self.rect.top, rect.width, rect.height))
    
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
###return Button(text, font = typeStyleComment, action = lambda: shell.show_screen(screen))
#  
##buttons = [
###screen_button("Build", shell.build_screen),
###screen_button("Units", shell.unit_screen),
###Button("Colonise", font = typeStyleComment, action = self.event.notify("colonise_planet", self.planet))
##]   
##buttons[0].enabled = not (self.planet.colony==None)
##buttons[1].enabled = not (self.planet.colony==None)##
##
##title = Label(shell.titletext)
##title.font = typeStyleTitle
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
##self.buttons.append(Button("Add Mine", font = typeStyleComment,
#########action = self.event.notify("mine_request", self.planet.colony)));

##for b in self.possbuilds:
###self.buttons.append(Button("" + b.type, font = typeStyleComment,
#########action = self.event.notify("building_request", self.planet.colony, b.type)))
##self.buttons.append(Button("Back",font=typeStyleComment, action = self.back))
##title.font = typeStyleTitle
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
###return Button(text, font = typeStyleTitle, action = lambda: shell.show_screen(screen))#   
##title = Label(shell.titletext)
##title.font = typeStyleTitle
#  
##for u in self.possunits:
###self.buttons.append(Button("" + u.type, font = typeStyleComment,
#########action = self.event.notify("unit_request", self.planet.colony, u.type)))
  
##self.buttons.append(Button("Back",font=typeStyleComment, action = self.back))
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
##self.buttons.append(Button("Back",font=typeStyleComment, action = self.back))
 

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
