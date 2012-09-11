class Unit:
    def __init__(self, colony):
        self._colony = colony
    
    def update(self):
        pass
    
    def production(self):
        return 0
    
    def transportable(self):
        return True

class Drone(Unit):
    def __init__(self, colony, ergs):
        Unit.__init__(self, colony)
        self._ergs = ergs
    
    def production(self):
        return self._ergs

class Ship(Unit):
    def __init__(self, colony, capacity):
        Unit.__init__(self, colony)
        self._capacity = capacity
        self._payloadType = ""
        self._payload = None
        self._destination = None
        self._fuel = 0
    
    def transportable(self):
        return False
    
    def update(self):
        if self._payloadType:
            self._fuel = 0
            self._colony = self._destination.colony
            self._destination = None
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

    def go(self, dest):
        fuelCost = self._colony.costTo(dest)*(self._capacity+1)
        if self._colony.fuel >= fuelCost - self._fuel:
            self._colony.fuel -= fuelCost - self._fuel
            self._fuel = fuelCost
            self._destination = dest
            return True
        else:
            print("Not enough fuel for trip")
            return False
    
    def loadMetal(self, amount):
        if self._payloadType:
            print("Unble to load Metal: %s already loaded"%self._payloadType)
            return
        if self._colony.metal < amount:
            print("Unble to load Metal: not enough metal available")
            return
        if amount > self._capacity:
            print("Unble to load Metal: over capacity")
            return
        self._payloadType = "Metal"
        self._payload = amount
        self._colony.metal -= amount

    def loadFood(self, amount):
        if self._payloadType:
            print("Unble to load Food: %s already loaded"%self._payloadType)
            return
        if self._colony.food < amount:
            print("Unble to load Food: not enough food available")
            return
        if amount > self._capacity:
            print("Unble to load Food: over capacity")
            return
        self._payloadType = "Food"
        self._payload = amount
        self._colony.food -= amount

    def loadFuel(self, amount):
        if self._payloadType:
            print("Unble to load Fuel: %s already loaded"%self._payloadType)
            return
        if self._colony.fuel < amount:
            print("Unble to load Fuel: not enough fuel available")
            return
        if amount > self._capacity:
            print("Unble to load Fuel: over capacity")
            return
        self._payloadType = "Fuel"
        self._payload = amount
        self._colony.fuel -= amount
        
    def loadUnit(self, unit):
        if self._payloadType and self._payloadType != "Unit":
            print("Unble to load Unit: %s already loaded"%self._payloadType)
            return
        if not self._colony.hasUnit(unit):
            print("Unble to load Unit: unit not here")
            return
        if not unit.transportable():
            print("Unble to load Unit: unit not transportable")
            return
        if not self._payloadType:
            self._payloadType = "Units"
            self._payload = []
        if len(self._payload) >= self._capacity:
            print("Unble to load Unit: over capacity")
            return
        self._payload.append(unit)
        self._colony.removeUnit(unit)
