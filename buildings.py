from collections import deque

def buildings():
    for (name, o) in globals().iteritems():
        try:
            if (o != Building) and issubclass(o, Building):
                yield name, o
        except TypeError: pass

class Building:
    name = "Building"
    ergCost = 10
    metalCost = 0
    foodCost = 0
    fuelCost = 0

    def __init__(self, eventmanager, colony):
        self._event = eventmanager
        self.colony = colony
    
    def update(self, processed):
        processed.append(self)
    
    def production(self):
        return 0

class Manufactory(Building):
    name = "Manufactory"
    metalCost = 2
    ergRate = 1
    
    def __init__(self, eventmanager, colony):
        Building.__init__(self, eventmanager, colony)
        self.ergs = 0
        self._queue = deque([])
    
    def construct(self, unit):
        if self.okay(unit):
            self._queue.append(unit)
    
    def update(self, processed):
        if len(self._queue) > 0:
            self.ergs += self.ergRate
            while len(self._queue) > 0 and (not self.okay(self._queue[0]) or self.ergs >= self._queue[0].ergCost):
                self.done(self._queue.popleft())
        else:
            self.ergs = 0
        Building.update(self, processed)

    def okay(self, unit):
        return (self.colony.metal >= unit.metalCost and
                self.colony.fuel >= unit.fuelCost and
                self.colony.food >= unit.foodCost)
    
    def done(self, unit):
        if self.okay(unit):
            self.ergs -= unit.ergCost
            self.colony.metal -= unit.metalCost
            self.colony.fuel -= unit.fuelCost
            self.colony.food -= unit.foodCost
            self.colony.addUnit(unit(self._event, self.colony))
    

class ReclamationFacility(Building):
    name = "Reclamation Facility"
    metalCost = 1
    def reclaim(self, unit):
        if not self.colony.hasUnit(unit):
            print("Unable to reclaim unit: unit not present")
            return
        self.colony.removeUnit(unit)
        self.colony.metal += unit.metalCost

class FuelExtractor(Building):
    name = "Fuel Extractor"
    def update(self, processed):
        count = 0
        for b in processed:
            if isinstance(b,FuelExtractor):
                count += 1
        if count < 5:
            amount = min(10 - 2*count, self.colony.planet.fuel)
            self.colony.planet.fuel -= amount
            self.colony.fuel += amount
        Building.update(self, processed)

class HydroponicsModule(Building):
    name = "Hydroponics Module"
    def update(self, processed):
        count = 0
        for b in processed:
            if isinstance(b,HydroponicsModule):
                count += 1
        if count < 5:
            amount = 10 - 2*count*self.colony.planet.food
            self.colony.food += amount
        Building.update(self, processed)

# class FuelStorage(Building):
#     pass

# class FoodSilo(Building):
#     pass
