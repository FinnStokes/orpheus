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
    def __init__(self, colony):
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
    
    def __init__(self, colony):
        Unit.__init__(self, colony)
        self._destination = None
        self._fuel = 0
    
    def transportable(self):
        return False
    
    def update(self, processed):
        if self._destination:
            self._fuel = 0
            self._colony.removeUnit(self)
            self._colony = self._destination.colony
            self._colony.addUnit(self)
            self._destination = None
        Unit.update(self, processed)
    
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
    
    def __init__(self, colony):
        Ship.__init__(self, colony)
        self._payloadType = ""
        self._payload = None
        self.fuelFactor = self.capacity+1
    
    def update(self, processed):
        Ship.update(self, processed)
        if self._payloadType:
            self.unload()
    
    def unload(self):
        if self._payloadType == "Metal":
            self._colony.metal += self._payload
        elif self._payloadType == "Food":
            self._colony.food += self._payload
        elif self._payloadType == "Fuel":
            self._colony.fuel += self._payload
        elif self._payloadType == "Units":
            for u in self._payload:
                self._colony.addUnit(u)
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

class Settler(Ship):
    metalCost = 2
    fuelFactor = 4
    
    def update(self, processed):
        if self._destination and not self._destination.colony:
            newColony = Colony(self._destination)
            self._fuel = 0
            self._destination = None
            self._colony.removeUnit(self)
        else:
            Ship.update(self, processed)

class Scout(Ship):
    metalCost = 1
    fuelFactor = 1