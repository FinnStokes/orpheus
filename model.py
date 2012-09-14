import event
import colony
import planet
import units
import buildings
import system

class Model:

    def __init__(self, eventmanager):
        self.event = eventmanager
        self.system = system.System(eventmanager,0)
        self.event.register("new_turn", self.update)
    
    def update():
        self.system.update()
