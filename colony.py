from collections import deque
import units

class Colony:
    def __init__(self, planet):
        if not planet.colony:
            self.planet = planet
            planet.colony = self
        self._metal = 0
        self._fuel = 0
        self._food = 0
        self._production = 1
        self.queue = deque([])
        self._buildings = []
        self._units = []
    
    def update(self):
        for b in self._buildings:
            b.update(self)
        for u in self._units:
            u.update(self)
        if len(self.queue) > 0:
            project = self.queue[0]
            done = project.work(self.production(), self)
            if done:
                self.queue.popleft()
    
    def metal(self):
        return self._metal
    
    def fuel(self):
        return self._fuel
    
    def food(self):
        return self._food
    
    def production(self):
        ergs = self._production
        for b in self._buildings:
            ergs += b.production(self)
        for u in self._units:
            ergs += u.production(self)
        return ergs

    def build(self, project):
        okay = project.okay(self)
        if okay:
            self.queue.append(project)
            return True
        return False
    
    def __str__(self):
        return "Colony(mt=%i, fl=%i, fd=%i, pr=%i)"%(self.metal(),self.fuel(),self.food(),self.production())

class Project:
    def __init__(self, ergs):
        self.ergs = ergs
    
    def work(self, ergs, colony):
        if not self.okay(colony):
            return True
        self.ergs -= ergs
        if self.ergs < 0:
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
        return colony.planet.metal > 0
    
    def done(self, colony):
        if self.okay(colony):
            colony.planet.metal -= 1
            colony._metal += 1

class BuildDrone(Project):
    def __init__(self):
        Project.__init__(self, 10)
    
    def okay(self, colony):
        return colony._metal >= 1
    
    def done(self, colony):
        if self.okay(colony):
            colony._metal -= 1
            colony._units.append(units.Drone(1))
