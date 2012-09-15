import colony

class Planet:
    def __init__(self, eventmanager, name, description, planet_type, planet_radius, mass, orbit_radius, orbit_phase, metal, fuel, food):
        self._event = eventmanager
        self.name = name
        self.description = description
        self.planet_type = planet_type
        self.planet_radius = planet_radius
        self.mass = mass
        self.orbit_radius = orbit_radius
        self.orbit_phase = orbit_phase
        self.colony = None
        self.links = {}
        self.metal = metal
        self.fuel = fuel
        self.food = food
    
    def update():
        if self.colony:
            self.colony.update()
    
    def addLink(self, planet, fuelCost):
        self.links[planet] = fuelCost
    
    def colonise(self):
        colony.Colony(self._event, self)

    def __str__(self):
        return "%s: %s"%(self.name,self.description)
    
    def __repr__(self):
        return "%s (t=%s, r=%f, m=%f, or=%f, ot=%f): m=%i, fu=%i, fo=%i"%(self.name,self.planet_type,self.planet_radius,self.mass,self.orbit_radius,self.orbit_phase,self.metal,self.fuel,self.food)
