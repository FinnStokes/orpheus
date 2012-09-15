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

# new_link(from, to, cost)
# Called when a new link is added between two planets in the system 

# new_colony(colony)
# Called when a new colony is established on a planet in the system 

# resourceupdate(planet, resourceid, amount)
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

# build_mine(planet)
# build a mine on the given planet

# build(planet,building)
# build the given building on the given planet

# build_unit(planet,unit)
# build the given unit on the given planet

# reclaim_unit(unit)
# reclaim the given unit, converting it to metal

# mine_built(planet)
# notification that a mine has been successfully constructed

# built(planet,building)
# notification that a building has been successfully constructed

# unit_built(planet,unit)
# notification that a unit has been successfully constructed

# unit_destroyed(unit)
# notification that a unit has been removed

# unit_moved(unit, to)

# transport(ship, dest)
# 

# queueproject(projectid, colony)
# 

# completeproject(projectid, colony)
# notification that a project has been successfully completed

#
#



