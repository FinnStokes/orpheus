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

# load(ship, resource_name, amount)
# Load some resources onto a ship

# load_unit(transport, target)
# Load target unit onto given transport

# unload(ship)
# Unload all resources from a docked ship

# build_mine(planet)
# Build a mine on the given planet

# build(planet,building)
# Build the given building on the given planet

# build_unit(planet,unit)
# Build the given unit on the given planet

# reclaim_unit(unit)
# Reclaim the given unit, converting it to metal

# mine_built(planet)
# Notification that a mine has been successfully constructed

# built(planet,building)
# Notification that a building has been successfully constructed

# unit_built(planet,unit)
# Notification that a unit has been successfully constructed

# unit_destroyed(unit)
# Notification that a unit has been removed

# unit_moved(unit, to)
# Notification that a unit has been moved to a given planet. 

# unit_queued(planet, unit)
# Notification that a unit has been accepted into the build queue

# move(ship, dest)
# 

#
#



