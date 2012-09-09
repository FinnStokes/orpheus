class Unit:
    def __init__(self):
        pass
    
    def update(self, colony):
        pass
    
    def production(self, colony):
        return 0

class Drone(Unit):
    def __init__(self, ergs):
        Unit.__init__(self)
        self._ergs = ergs
    
    def production(self, colony):
        return self._ergs

class Ship(Unit):
    def __init__(self):
        Unit.__init__(self)
