from collections import deque

class Colony:
    def __init__(self, eventmanager, planet):
        if not planet.colony:
            self.planet = planet
            planet.colony = self
        self._event = eventmanager
        self._event.register("build_mine",self.handle_build_mine)
        self._event.register("build",self.handle_build)
        self.metal = 0
        self.fuel = 0
        self.food = 0
        self._production = 1
        self.queue = deque([])
        self._buildings = []
        self._units = []
        self._addUnits = []
        self._delUnits = []
    
    def update(self):
        processed = []
        for b in self._buildings:
            b.update(processed)
        processed = []
        for u in self.units():
            u.update(processed)
        if len(self.queue) > 0:
            project = self.queue[0]
            done = project.work(self.production(), self)
            if done:
                self.queue.popleft()
    
    def production(self):
        ergs = self._production
        for b in self._buildings:
            ergs += b.production()
        for u in self.units():
            ergs += u.production()
        return ergs
    
    def handle_build_mine(self, planet):
        if planet == self.planet:
            self.buildMine()

    def handle_build(self, planet, building):
        if planet == self.planet:
            self.build(building)

    def buildMine(self):
        self.do(BuildMine(self._event))
    
    def build(self, building):
        self.do(BuildBuilding(self._event,building))

    def do(self, project):
        okay = project.okay(self)
        if okay:
            self.queue.append(project)
            return True
        return False

    def getBuildings(self, building):
        ret = []
        for b in self._buildings:
            if isinstance(b,building):
                ret.append(b)
        return ret

    def units(self):
        for a in self._addUnits:
            self._units.append(a)
        self._addUnits = []
        for d in self._delUnits:
            self._units.remove(d)
        self._delUnits = []
        return self._units
    
    def getUnit(self, i):
        return self.units()[i]

    def addUnit(self, unit):
        self._addUnits.append(unit)

    def hasUnit(self, unit):
        return unit in self.units()
    
    def removeUnit(self, unit):
        self._delUnits.append(unit)
    
    def costTo(self, planet):
        return self.planet.links[planet]
    
    def __repr__(self):
        return "Colony(mt=%f, fl=%f, fd=%f, pr=%f)"%(self.metal,self.fuel,self.food,self.production())

class Project:
    def __init__(self, eventmanager, ergs):
        self._event = eventmanager
        self.ergs = ergs
    
    def work(self, ergs, colony):
        if not self.okay(colony):
            self.fail(colony)
            return True
        self.ergs -= ergs
        if self.ergs <= 0:
            self.done(colony)
            return True
        return False
    
    def okay(self, colony):
        return True
    
    def done(self, colony):
        pass

    def fail(self, colony):
        pass

class BuildMine(Project):
    def __init__(self, eventmanager):
        Project.__init__(self, eventmanager, 10)
    
    def okay(self, colony):
        return colony.planet.metal >= 1
    
    def done(self, colony):
        if self.okay(colony):
            colony.planet.metal -= 1
            colony.metal += 1
            self._event.notify("mine_built",colony.planet)

    def fail(self, colony):
        self._event.notify("mine_cancelled",colony.planet)

# class BuildUnit(Project):
#     def __init__(self, eventmanager, unit):
#         Project.__init__(self, eventmanager, unit.ergCost)
#         self.unit = unit
    
#     def okay(self, colony):
#         return (colony.metal >= self.unit.metalCost and
#                 colony.fuel >= self.unit.fuelCost and
#                 colony.food >= self.unit.foodCost)
    
#     def done(self, colony):
#         if self.okay(colony):
#             colony.metal -= self.unit.metalCost
#             colony.fuel -= self.unit.fuelCost
#             colony.food -= self.unit.foodCost
#             u = self.unit(self._event, colony)
#             colony.addUnit(u)
#             self._event.notify("unit_built",colony.planet,u)

class BuildBuilding(Project):
    def __init__(self, eventmanager, building):
        Project.__init__(self, eventmanager, building.ergCost)
        self.building = building
    
    def okay(self, colony):
        return (colony.metal >= self.building.metalCost and
                colony.fuel >= self.building.fuelCost and
                colony.food >= self.building.foodCost)
    
    def done(self, colony):
        if self.okay(colony):
            colony.metal -= self.building.metalCost
            colony.fuel -= self.building.fuelCost
            colony.food -= self.building.foodCost
            b = self.building(self._event, colony)
            colony._buildings.append(b)
            self._event.notify("built",colony.planet,b)

    def fail(self, colony):
        self._event.notify("build_cancelled",colony.planet,b)
