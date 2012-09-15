import pygame, sys

class Widget:
    def __init__(self, x, y, eventmanager, render):
        self.x = x
        self.y = y
        self.w = 0
        self.h = 0
        self.children = []
        self.event = eventmanager
        self.event.register("update_widget", self.update)

    def update(self):
        self.update_pos(self)   

    def update_pos(self, obj):
        for i in range(0, len(obj.children)):
            parent = obj.children[i].parent           
            child = obj.children[i]
            
            y = parent.y + parent.h 
            
            child.y = y
            
            if i > 0: 
                for j in range(0, i):
                    child.y += parent.children[j].get_childrens_height();

            self.update_pos(child);                                     
      
    def draw(self):
        for i in range(0, len(self.children)):
            if self.children[i].visible: 
                self.children[i].draw()

    def add(self, parent, child):
        child.parent = parent
        parent.children.append(child)                      
 
    def rect():
        pygame.Rect(self.x, self.y, self.w,self.h)
       

class Menu:

    pygame.font.init()
    TEXT_OFFSET = (5, 5)
    myfont = pygame.font.Font("res/fonts/8bit_nog.ttf", 18)
 
    def __init__(self, id, w, h, eventmanager, render, text, action, visible = False, colour = pygame.Color("white")):
        self.id = id
        self.x = 0
        self.y = 0        
        self.w = w        
        self.h = h       
        self.children = [] 
        self.event = eventmanager
        self.render = render
        self.visible = visible
        self.text = text
        self.TEXT_OFFSET = Menu.TEXT_OFFSET
        self.font = Menu.myfont
        self.colour = colour
        self.event.register("mouse_up", self.mouse_up)              
        
        if action == None:
            self.hasevent = False
            self.action = self.expose_children
        else:
            self.hasevent = True
            self.action = action
           
    def update(self):
        Widget.update_pos(self)

    def draw(self):
        if self.visible:
        #draw box, then text
            pygame.draw.rect(self.render.window, self.colour, (self.x, self.y, self.w, self.h))                 
            self.render.window.blit(self.font.render(self.text, 1, (0,0,0)), (self.x, self.y, self.w, self.h))
     
        

    def add(self, child):
        child.parent = self
        self.children.append(child)

    def expose_children(self):
        for c in range(0, len(self.children)):
            self.children[c].visible = True   
        self.action = self.hide_children
        self.event.notify("update_widget")

    def hide_children(self):
        for c in range(0, len(self.children)):
            self.children[c].visible = False
        self.action = self.expose_children
        self.event.notify("update_widget")
         
    def mouse_up(self, pos, button):
        if button == 1 and self.is_on(pos):
            if self.hasevent:
                self.event.notify(self.action[0], self.action[1])
            else:
                self.action()
        

    def is_on(self, pos):
        res = (pos[0] >= self.x) and (pos[0] <= self.x + self.w)
        res = res and (pos[1] >= self.y) and (pos[1] <= self.y + self.h)        
        return res

    def get_childrens_height(self):
        parent = self
        totalheight = parent.h
    
        for i in range(0, len(parent.children)):
            if parent.children[i].visible:
                totalheight += parent.children[i].get_childrens_height()
        return totalheight
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
