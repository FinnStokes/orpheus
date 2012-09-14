class EventManage:
    def __init__(self):
        self.handlers = dict()     
        self.events = []

    def register(self, event, handler):
        if not event in self.handlers:
            self.handlers[event] = []
        
        if not handler in self.handlers[event]:
            self.handlers[event].append(handler)
        return self

    def deregister(self, event, handler):       
        if not event in self.handlers:
            raise ValueError("Event is not registered")
        try:
            self.handlers[event].remove(handler)
        except:
            raise ValueError("Handler is not registered with this event.")
        return self

    def notify(self, event, *args, **kargs):   
        self.events.append((event, args, kargs))
  
    def update(self):
        for e in self.events:
            if e[0] in self.handlers:
                for h in self.handlers[e[0]]:
                    h(*e[1], **e[2]) 
        self.events = []

# Events
#

# update(dt)
# Called periodically with dt set to the time in seconds it was last produced

# new_turn()
# Called when a turn is ended, causing model to update

# key_down(keyid)
# Called when a key is pressed, keyid to be interpreted by pygame.locals 

# key_up(keyid)
# Called when a key is released, keyid to be interpreted by pygame.locals 

# new_planet(planet)
# Called when a new planet is added to the system 

# resourceupdate(resourceid, amount)
# Update available amount of a resource, for reflection in interface

# colonise(planet)
# Establish a colony on an uncolonised planet

# abandon(planet)
# Remove colony and improvements from a planet

# loadship(ship, resources)
# load some resources onto a ship

# unloadship(ship)
# unload all resources from a docked ship

# upgradeship(colony, ship, upgrade)
# make an improvement to a ship via the as yet only suggested Astronautics Division building

# transport(ship, dest)
# 

# queueproject(projectid, colony)
# 

# completeproject(projectid, colony)
# notification that a project has been successfully completed

#
#



