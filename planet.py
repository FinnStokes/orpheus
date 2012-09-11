class Planet:
    def __init__(self, metal, fuel, food):
        self.colony = None
        self.links = {}
        self.metal = metal
        self.fuel = fuel
        self.food = food
    
    def addLink(self, planet, fuelCost):
        self.links[planet] = fuelCost

