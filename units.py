from colony import Colony

def units():
    for (name, o) in globals().iteritems():
        try:
            if (o != Unit) and issubclass(o, Unit):
                yield name, o
        except TypeError: pass

class Unit:
    ergCost = 10
    metalCost = 0
    foodCost = 0
    fuelCost = 0
    def __init__(self, eventmanager, colony):
        self._event = eventmanager
        self._colony = colony
    
    def update(self, processed):
        processed.append(self)
    
    def production(self):
        return 0
    
    def transportable(self):
        return True

class Drone(Unit):
    metalCost = 1
    ergRate = 1
    
    def production(self):
        return Drone.ergRate

class Ship(Unit):
    fuelFactor = 1
    
    def __init__(self, eventmanager, colony):
        Unit.__init__(self, eventmanager, colony)
        self._event.register("move", self.handle_move)
        self._destination = None
        self._fuel = 0
    
    def transportable(self):
        return False
    
    def update(self, processed):
        if self._destination:
            if self._destination.colony:
                self._event.notify("unit_moved", self, self._destination)
                self._fuel = 0
                self._colony.removeUnit(self)
                self._colony = self._destination.colony
                self._colony.addUnit(self)
                self._destination = None
            else:
                print("Invalid destination: no colony")
        Unit.update(self, processed)
    
    def handle_move(self, unit, dest):
        if unit == self and dest != self._colony.planet:
            self.go(dest)
    
    def go(self, dest):
        fuelCost = self._colony.costTo(dest)*self.fuelFactor
        if self._colony.fuel >= fuelCost - self._fuel:
            self._colony.fuel -= fuelCost - self._fuel
            self._fuel = fuelCost
            self._destination = dest
            return True
        else:
            print("Not enough fuel for trip")
            return False

class Transport(Ship):
    metalCost = 1
    capacity = 1
    
    def __init__(self, eventmanager, colony):
        Ship.__init__(self, eventmanager, colony)
        self._event.register("load", self.handle_load)
        self._event.register("load_unit", self.handle_load_unit)
        self._event.register("unload", self.handle_unload)
        self._payloadType = ""
        self._payload = None
        self.fuelFactor = self.capacity+1
    
    def update(self, processed):
        Ship.update(self, processed)
        if self._payloadType:
            self.unload()
    
    def handle_load(self, unit, resource, amount):
        if unit == self:
            if resource == "Metal":
                self.loadMetal(amount)
            elif resource == "Food":
                self.loadFood(amount)
            elif resource == "Fuel":
                self.loadFuel(amount)
    
    def handle_unload(self, unit):
        if unit == self:
            self.unload()
    
    def handle_load_unit(self, transport, target):
        if transport == self:
            self.loadUnit(target)
    
    def unload(self):
        if self._payloadType == "Metal":
            self._colony.metal += self._payload
            self._event.notify("resourceupdate", self._colony.planet, "metal", self._colony.metal)
        elif self._payloadType == "Food":
            self._colony.food += self._payload
            self._event.notify("resourceupdate", self._colony.planet, "food", self._colony.food)
        elif self._payloadType == "Fuel":
            self._colony.fuel += self._payload
            self._event.notify("resourceupdate", self._colony.planet, "fuel", self._colony.fuel)
        elif self._payloadType == "Units":
            for u in self._payload:
                self._colony.addUnit(u)
                u._colony = self._colony
                self._event.notify("unit_moved", u, self._colony.planet)
        self._payloadType = ""
        self._payload = None
    
    def loadMetal(self, amount):
        if self._payloadType:
            self.unload()
        if amount > self._colony.metal:
            amount = self._colony.metal
        if amount > self.capacity:
            amount = self.capacity
        self._payloadType = "Metal"
        self._payload = amount
        self._colony.metal -= amount
        self._event.notify("resourceupdate", self._colony.planet, "metal", self._colony.metal)

    def loadFood(self, amount):
        if self._payloadType:
            self.unload()
        if amount > self._colony.food:
            amount = self._colony.food
        if amount > self.capacity*100:
            amount = self.capacity*100
        self._payloadType = "Food"
        self._payload = amount
        self._colony.food -= amount
        self._event.notify("resourceupdate", self._colony.planet, "food", self._colony.food)

    def loadFuel(self, amount):
        if self._payloadType:
            self.unload()
        if amount > self._colony.fuel:
            amount = self._colony.fuel
        if amount > self.capacity*100:
            amount = self.capacity*100
        self._payloadType = "Fuel"
        self._payload = amount
        self._colony.fuel -= amount
        self._event.notify("resourceupdate", self._colony.planet, "fuel", self._colony.fuel)
        
    def loadUnit(self, unit):
        if self._payloadType and self._payloadType != "Units":
            self.unload()
        if not self._colony.hasUnit(unit):
            print("Unble to load Unit: unit not here")
            return
        if not unit.transportable():
            print("Unble to load Unit: unit not transportable")
            return
        if not self._payloadType:
            self._payloadType = "Units"
            self._payload = []
        if len(self._payload) >= self.capacity:
            print("Unble to load Unit: over capacity")
            return
        self._payload.append(unit)
        self._colony.removeUnit(unit)
        self._event.notify("unit_moved", unit, None)

class Settler(Ship):
    metalCost = 2
    fuelFactor = 4
    
    def update(self, processed):
        if self._destination and not self._destination.colony:
            self._destination.colonise()
            self._fuel = 0
            self._destination = None
            self._colony.removeUnit(self)
            self._event.notify("unit_destroyed", self)
        else:
            Ship.update(self, processed)

class Scout(Ship):
    metalCost = 1
    fuelFactor = 1
