def buildings():
    for (name, o) in globals().iteritems():
        try:
            if (o != Building) and issubclass(o, Building):
                yield name, o
        except TypeError: pass

class Building:
    ergCost = 10
    metalCost = 0
    foodCost = 0
    fuelCost = 0
    def __init__(self, colony):
        self.colony = colony
    
    def update(self, processed):
        processed.append(self)

class Manufactory(Building):
    metalCost = 2
    def construct(self, unit):
        pass

class ReclamationFacility(Building):
    metalCost = 1
    def reclaim(self, unit):
        pass

class FuelExtractor(Building):
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
