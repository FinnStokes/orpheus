import random
import randNames
import desc
import planet
import math
import event

NAMES = [ 'Quo', 'Usque', 'Tandem', 'Abutere', 'Catilina', 'Patientia', 'Nostra', 'Quam', 'Diu', 'Etiam', 'Furor',
'Iste', 'Tuus', 'Nos', 'Eludet', 'Quem', 'Ad', 'Finem', 'Sese', 'Effrenata', 'Iactabit', 'Audacia', 'Nihilne',
 'Te', 'Nocturnum', 'Praesidium', 'Palati', 'Nihil', 'Urbis', 'Vigiliae', 'Nihil', 'Timor', 'Populi', 'Concursus',
'Bonorum', 'Omnium', 'Hic', 'Munitissimus', 'Habendi', 'Senatus', 'Locus', 'Horum', 'Ora', 'Voltusque', 'Moverunt', 'Patere', 'Tua', 'Consilia', 'Non', 'Sentis', 'Constrictam', 'Iam', 'Scientia', 'Teneri', 'Coniurationem',
'Tuam', 'Vides', 'Quid', 'Proxima', 'Superiore', 'Nocte', 'Egeris', 'Ubi', 'Fueris', 'Quos', 'Convocaveris', 'Consilii', 'Ceperis', 'Quem', 'Nostrum', 'Ignorare', 'Arbitraris'
]



class System:
    def __init__(self, eventmanager, seed):
        random.seed(seed)
        self._event = eventmanager
        self._names = randNames.MName(2,NAMES)
        self.starName = self._randomName()
        self.planets = []
        r = 0
        # Inner planets
        nInner = random.randint(3,6)
        for i in range(0,nInner):
            r = self._newTerrestrialPlanet(r)
        
        r = self._newAsteroidField(r)
        
        nOuter = random.randint(3,6)
        for i in range(0,nOuter):
            r = self._newGasPlanet(r)
    
    def update():
        for p in planets:
            p.update()
    
    def _newTerrestrialPlanet(self,r):
        name = self._randomName()
        description = self._randomDescription(name,"terrestrial planet")
        planet_radius = random.triangular(0.5,2.0)
        planet_mass = planet_radius*planet_radius*planet_radius*random.triangular(0.9,1.1)
        orbit_radius = r + random.triangular(0.2,0.8)
        orbit_phase = random.uniform(0,2*math.pi)
        metal = random.randint(5,7)
        fuel = random.randint(0,3)*50
        food = random.randint(13,20)*5
        p = planet.Planet(self._event,name,description,"terrestrial planet",planet_radius,planet_mass,orbit_radius,orbit_phase,metal,fuel,food)
        self.planets.append(p)
        self._event.notify("new_planet",p)
        return orbit_radius
    
    def _newGasPlanet(self,r):
        name = self._randomName()
        description = self._randomDescription(name,"gas giant")
        planet_radius = random.triangular(3.0,20.0,5.0)
        planet_mass = planet_radius*planet_radius*planet_radius*random.triangular(0.15,0.25)
        orbit_radius = r + random.triangular(4.0,10.0)
        orbit_phase = random.uniform(0,2*math.pi)
        metal = 0
        fuel = random.randint(6,14)*50
        food = random.randint(1,5)*5
        p = planet.Planet(self._event,name,description,"gas giant",planet_radius,planet_mass,orbit_radius,orbit_phase,metal,fuel,food)
        self.planets.append(p)
        self._event.notify("new_planet",p)
        return orbit_radius
    
    def _newAsteroidField(self,r):
        self.asteroid_radius = r + random.triangular(0.5,2.0)
        n = random.randint(5,8)
        offset = random.uniform(0,2*math.pi)
        t = [math.fmod(x*math.pi/8,math.pi*2) + offset for x in range(0,16)]
        random.shuffle(t)
        for i in range(0,n):
            self._newDwarfPlanet(self.asteroid_radius,t[i])
        return self.asteroid_radius
    
    def _newDwarfPlanet(self,r,t):
        name = self._randomName()
        description = self._randomDescription(name,"dwarf planet")
        planet_radius = random.triangular(0.05,0.20)
        planet_mass = planet_radius*planet_radius*planet_radius*random.triangular(0.45,0.55)
        orbit_radius = r + random.triangular(-0.1,0.1)
        orbit_phase = t + random.triangular(-math.pi/32.0,math.pi/32.0)
        metal = random.randint(5,7)
        fuel = 0
        food = random.randint(3,10)*5
        p = planet.Planet(self._event,name,description,"dwarf planet",planet_radius,planet_mass,orbit_radius,orbit_phase,metal,fuel,food)
        self.planets.append(p)
        self._event.notify("new_planet",p)
    
    def _randomName(self):
        return self._names.New()

    def _randomDescription(self,name,planet_type):
        return desc.random_description(name, planet_type)

if __name__ == '__main__':
    s = System(event.EventManage(), 0)
    for p in s.planets:
        print(p)
        print(repr(p)+"\n")
