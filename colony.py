from collections import deque
import units

class Colony:
    def __init__(self, planet):
        if not planet.colony:
            self.planet = planet
            planet.colony = self
        self.metal = 0
        self.fuel = 0
        self.food = 0
        self._production = 1
        self.queue = deque([])
        self._buildings = []
        self._units = []
    
    def update(self):
        for b in self._buildings:
            b.update()
        for u in self._units:
            u.update()
        if self.planet.fuel >= 1:
            self.planet.fuel -= 1
            self.fuel += 1
        if len(self.queue) > 0:
            project = self.queue[0]
            done = project.work(self.production(), self)
            if done:
                self.queue.popleft()
    
    def production(self):
        ergs = self._production
        for b in self._buildings:
            ergs += b.production()
        for u in self._units:
            ergs += u.production()
        return ergs

    def build(self, project):
        okay = project.okay(self)
        if okay:
            self.queue.append(project)
            return True
        return False
    
    def addUnit(self, unit):
        self._units.append(unit)

    def getUnit(self, i):
        return self._units[i]

    def hasUnit(self, unit):
        return unit in self._units
    
    def removeUnit(self, unit):
        self._units.remove(unit)
    
    def costTo(self, planet):
        return self.planet.links[planet]
    
    def __repr__(self):
        return "Colony(mt=%f, fl=%f, fd=%f, pr=%f)"%(self.metal,self.fuel,self.food,self.production())

class Project:
    def __init__(self, ergs):
        self.ergs = ergs
    
    def work(self, ergs, colony):
        if not self.okay(colony):
            print("Project cancelled: Insufficient resources")
            return True
        self.ergs -= ergs
        if self.ergs <= 0:
            print("Project complete")
            self.done(colony)
            return True
        return False
    
    def okay(self, colony):
        return True
    
    def done(self, colony):
        pass
    
class BuildMine(Project):
    def __init__(self):
        Project.__init__(self, 10)
    
    def okay(self, colony):
        return colony.planet.metal >= 1
    
    def done(self, colony):
        if self.okay(colony):
            colony.planet.metal -= 1
            colony.metal += 1

class BuildDrone(Project):
    def __init__(self):
        Project.__init__(self, 10)
    
    def okay(self, colony):
        return colony.metal >= 1
    
    def done(self, colony):
        if self.okay(colony):
            colony.metal -= 1
            colony.addUnit(units.Drone(colony, 1))

class BuildShip(Project):
    def __init__(self):
        Project.__init__(self, 10)
    
    def okay(self, colony):
        return colony.metal >= 1
    
    def done(self, colony):
        if self.okay(colony):
            colony.metal -= 1
            colony.addUnit(units.Ship(colony, 1))
