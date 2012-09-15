import pygame, sys

class Widget:
    def __init__(self, x, y, eventmanager, render):
        self.x = x
        self.y = y
        self.w = 0
        self.h = 0
        self.children = []
        self.event = eventmanager

    def update(self):
        self.update_pos(self)   

    def update_pos(self, obj):
        for i in range(0, len(self.children)):
            parent = self.children[i].parent           
            child = self.children[i]
            y = parent.y + parent.h 
            
            child.y = y
            
            if i > 0: 
                for j in range(0, i):
                    child.y += parent.children[j].getChildrensHeight();

            update_pos(child);                                     
      
    def draw(self):
        for i in range(0, len(self.children)):
            if self.children[i].visible: 
                self.children[i].draw()

    def add(self, parent, child):
        obj.parent = parent
        parent.children.append(child)                      
        

class Menu:

    pygame.font.init()
    TEXT_OFFSET = (5, 5)
    myfont = pygame.font.Font("res/fonts/8bit_nog.ttf", 20)
 
    def __init__(self, id, w, h, eventmanager, render, text, action, visible = False, colour = pygame.Color("white")):
        self.id = id
        self.x = 0
        self.y = 0        
        self.w = w        
        self.h = h       
        self.children = [] 
        self.event = eventmanager
        self.render = render
        self.text = text
        self.TEXT_OFFSET = Menu.TEXT_OFFSET
        self.font = myfont
        self.colour = colour
        self.event.register("mouse_up", self.mouse_up)              
    
        if action == None:
            self.action = self.expose_children
        else:
            self.action = action
           
    def update(self):
        Widget.update_pos(self)

    def draw(self):
        if self.visible:
        #draw box, then text
            pygame.draw(self.render.window, colour, (self.x, self.y, self.w, self.h)) 
                 
            self.render.window.blit(self.font.render(self.text, 1, (0,0,0)), (self.x, self.y, self.w, self.h))
            pygame.display.update()


    def add(self, child):
        child.parent = self
        self.children.append(child)

    def expose_children(self):
        for c in range(0, len(self.children)):
            c.visible = True   
        self.action = self.hide_children
    

    def hide_children(self):
        for c in range(0, len(self.children)):
            c.visible = False
        self.action = self.expose_children

         
    def mouse_up(self, pos, button):
        if button == 1 and is_on(pos):
            self.action()

    def is_on(self, pos):
        res = (pos.x >= self.x) and (pos.x <= self.x + self.w)
        res = res and (pos.y >= self.y) and (pos.x <= self.y + self.h)        
        return res



#Root

###Description
#####Display
##
###Resources
#####Display
##
###Buildings
#####Factory
#####Hydroponics
##
###Units
#####Worker
#####Transport
