import unittest
import planet
import colony
import units
import buildings

class TestColony(unittest.TestCase):
    def setUp(self):
        self.fuelRate = 1
        self.mineTime = 10
        self.droneTime = 10
        self.p1 = planet.Planet(5,0,0)
        self.c1 = colony.Colony(self.p1)
        self.p2 = planet.Planet(0,500,0)
        self.c2 = colony.Colony(self.p2)
        self.p3 = planet.Planet(0,0,150)
        self.c3 = colony.Colony(self.p3)
        self.initial = {}
        self.store(self.c1)
        self.store(self.c2)
        self.store(self.c3)
        
    def store(self, colony):
        self.initial[colony] = {
            'metal': colony.planet.metal,
            'fuel': colony.planet.fuel,
            'food': colony.planet.food,
            }
    
    def check_resources(self, colony, metal, fuel, food):
        self.assertEqual(colony.metal, metal)
        self.assertEqual(colony.fuel, fuel)
        self.assertEqual(colony.food, food)

    def check_gathered_resources(self, colony, metal, fuel, food):
        self.check_resources(colony, metal, fuel, food)
        self.assertEqual(colony.metal + colony.planet.metal, self.initial[colony]['metal'])
        self.assertEqual(colony.fuel + colony.planet.fuel, self.initial[colony]['fuel'])
        self.assertEqual(colony.food + colony.planet.food, self.initial[colony]['food'])
    
    def test_fuel(self):
        for i in range(0,20):
            self.c1.update()
            self.c2.update()
            self.c3.update()
        self.check_gathered_resources(self.c1,0,0,0)
        self.check_gathered_resources(self.c2,0,20*self.fuelRate,0)
        self.check_gathered_resources(self.c3,0,0,0)
        for i in range(0,500/self.fuelRate):
            self.c1.update()
            self.c2.update()
            self.c3.update()
        self.check_gathered_resources(self.c1,0,0,0)
        self.check_gathered_resources(self.c2,0,500,0)
        self.check_gathered_resources(self.c3,0,0,0)

    def test_metal(self):
        self.c1.build(colony.BuildMine())
        self.c2.build(colony.BuildMine())
        self.c3.build(colony.BuildMine())
        for i in range(0,self.mineTime):
            self.c1.update()
            self.c2.update()
            self.c3.update()
        self.check_gathered_resources(self.c1,1,0,0)
        self.check_gathered_resources(self.c2,0,self.mineTime,0)
        self.check_gathered_resources(self.c3,0,0,0)
        for j in range(0,5):
            self.c1.build(colony.BuildMine())
            self.c2.build(colony.BuildMine())
            self.c3.build(colony.BuildMine())
        for j in range(0,5):
            for i in range(0,self.mineTime):
                self.c1.update()
                self.c2.update()
                self.c3.update()
        self.check_gathered_resources(self.c1,5,0,0)
        self.check_gathered_resources(self.c2,0,6*self.mineTime,0)
        self.check_gathered_resources(self.c3,0,0,0)
    
    def test_drone(self):
        self.c1.build(colony.BuildMine())
        self.c2.build(colony.BuildMine())
        self.c3.build(colony.BuildMine())
        self.c1.build(colony.BuildMine())
        self.c2.build(colony.BuildMine())
        self.c3.build(colony.BuildMine())
        for i in range(0,self.mineTime*2):
            self.c1.update()
            self.c2.update()
            self.c3.update()
        self.c1.build(colony.BuildDrone())
        self.c2.build(colony.BuildDrone())
        self.c3.build(colony.BuildDrone())
        self.c1.build(colony.BuildDrone())
        self.c2.build(colony.BuildDrone())
        self.c3.build(colony.BuildDrone())
        self.c1.build(colony.BuildDrone())
        self.c2.build(colony.BuildDrone())
        self.c3.build(colony.BuildDrone())
        for i in range(0,self.droneTime):
            self.c1.update()
            self.c2.update()
            self.c3.update()
        self.assertEqual(self.c1.production(),2)
        self.assertEqual(self.c2.production(),1)
        self.assertEqual(self.c3.production(),1)
        for i in range(0,self.droneTime*2):
            self.c1.update()
            self.c2.update()
            self.c3.update()
        self.assertEqual(self.c1.production(),3)
        self.assertEqual(self.c2.production(),1)
        self.assertEqual(self.c3.production(),1)

if __name__ == '__main__':
    unittest.main()
