from collections import deque

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
    
    def update(self):
        if len(self.queue) > 0:
            project = self.queue[0]
            project.update(self.production())
            if project.ergs < 0:
                self.queue.popleft()
    
    def metal(self):
        return self._metal
    
    def fuel(self):
        return self._fuel
    
    def food(self):
        return self._food
    
    def production(self):
        return self._production

class Project:
    def __init__(self, ergs):
        self.ergs = ergs
    
    def update(self, ergs):
        self.ergs -= ergs
        if ergs < 0:
            self.done()
    
    def done(self):
        pass
    
