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
    
    def update(self, turns):
        for i in range(0,turns):
            self.c1.update()
            self.c2.update()
            self.c3.update()
    
    def assertResources(self, colony, metal, fuel, food):
        self.assertEqual(colony.metal, metal)
        self.assertEqual(colony.fuel, fuel)
        self.assertEqual(colony.food, food)

    def assertResourceConservation(self, colony):
        self.assertEqual(colony.metal + colony.planet.metal, self.initial[colony]['metal'])
        self.assertEqual(colony.fuel + colony.planet.fuel, self.initial[colony]['fuel'])
        self.assertEqual(colony.food + colony.planet.food, self.initial[colony]['food'])
    
    def test_fuel(self):
        self.update(20)
        self.assertResources(self.c1,0,0,0)
        self.assertResourceConservation(self.c1)
        self.assertResources(self.c2,0,20*self.fuelRate,0)
        self.assertResourceConservation(self.c2)
        self.assertResources(self.c3,0,0,0)
        self.assertResourceConservation(self.c3)
        self.update(500/self.fuelRate)
        self.assertResources(self.c1,0,0,0)
        self.assertResourceConservation(self.c1)
        self.assertResources(self.c2,0,500,0)
        self.assertResourceConservation(self.c2)
        self.assertResources(self.c3,0,0,0)
        self.assertResourceConservation(self.c3)

    def test_metal(self):
        self.c1.build(colony.BuildMine())
        self.c2.build(colony.BuildMine())
        self.c3.build(colony.BuildMine())
        self.update(self.mineTime)
        self.assertResources(self.c1,1,0,0)
        self.assertResourceConservation(self.c1)
        self.assertResources(self.c2,0,self.mineTime,0)
        self.assertResourceConservation(self.c2)
        self.assertResources(self.c3,0,0,0)
        self.assertResourceConservation(self.c3)
        for i in range(0,5):
            self.c1.build(colony.BuildMine())
            self.c2.build(colony.BuildMine())
            self.c3.build(colony.BuildMine())
        self.update(5*self.mineTime)
        self.assertResources(self.c1,5,0,0)
        self.assertResourceConservation(self.c1)
        self.assertResources(self.c2,0,6*self.mineTime,0)
        self.assertResourceConservation(self.c2)
        self.assertResources(self.c3,0,0,0)
        self.assertResourceConservation(self.c3)
    
    def test_drone(self):
        self.c1.build(colony.BuildMine())
        self.c2.build(colony.BuildMine())
        self.c3.build(colony.BuildMine())
        self.c1.build(colony.BuildMine())
        self.c2.build(colony.BuildMine())
        self.c3.build(colony.BuildMine())
        self.update(self.mineTime*2)
        self.c1.build(colony.BuildDrone())
        self.c2.build(colony.BuildDrone())
        self.c3.build(colony.BuildDrone())
        self.c1.build(colony.BuildDrone())
        self.c2.build(colony.BuildDrone())
        self.c3.build(colony.BuildDrone())
        self.c1.build(colony.BuildDrone())
        self.c2.build(colony.BuildDrone())
        self.c3.build(colony.BuildDrone())
        self.update(self.droneTime)
        self.assertEqual(self.c1.production(),2)
        self.assertEqual(self.c2.production(),1)
        self.assertEqual(self.c3.production(),1)
        self.update(self.droneTime*2)
        self.assertEqual(self.c1.production(),3)
        self.assertEqual(self.c2.production(),1)
        self.assertEqual(self.c3.production(),1)

class TestShip(unittest.TestCase):
    def setUp(self):
        self.shipTime = 10
        self.droneTime = 10
        self.p1 = planet.Planet(0,0,0)
        self.c1 = colony.Colony(self.p1)
        self.c1.metal = 1
        self.c1.fuel = 90
        self.c1.food = 150
        self.p2 = planet.Planet(0,0,0)
        self.c2 = colony.Colony(self.p2)
        self.c2.metal = 0
        self.c2.fuel = 150
        self.c2.food = 0
        self.p3 = planet.Planet(0,0,0)
        self.c3 = colony.Colony(self.p3)
        self.c3.metal = 5
        self.c3.fuel = 70
        self.c3.food = 0
        self.p1.addLink(self.p2,50/2)
        self.p1.addLink(self.p3,20/2)
        self.p2.addLink(self.p1,50/2)
        self.p2.addLink(self.p3,10/2)
        self.p3.addLink(self.p1,70/2)
        self.p3.addLink(self.p2,10/2)
    
    def update(self, turns):
        for i in range(0,turns):
            self.c1.update()
            self.c2.update()
            self.c3.update()
    
    def assertResources(self, colony, metal, fuel, food):
        self.assertEqual(colony.metal, metal)
        self.assertEqual(colony.fuel, fuel)
        self.assertEqual(colony.food, food)

    def runTest(self):
        self.c1.build(colony.BuildShip())
        self.c1.build(colony.BuildShip())
        self.c2.build(colony.BuildShip())
        self.c3.build(colony.BuildShip())
        self.update(self.shipTime*2)
        s1 = self.c1.getUnit(0)
        s2 = self.c3.getUnit(0)
        self.assertRaises(IndexError, self.c1.getUnit, 1)
        self.assertRaises(IndexError, self.c2.getUnit, 0)
        self.assertTrue(self.c1.hasUnit(s1))
        self.assertTrue(self.c3.hasUnit(s2))
        
        s1.loadFood(50)
        s1.loadFood(100)
        s1.go(self.p2)
        s2.loadMetal(1)
        s2.loadMetal(2)
        s2.go(self.p1)
        self.update(1)
        self.assertTrue(self.c2.hasUnit(s1))
        self.assertTrue(self.c1.hasUnit(s2))
        self.assertResources(self.c1,1,40,50)
        self.assertResources(self.c2,0,150,100)
        self.assertResources(self.c3,3,0,0)
        
        self.c1.build(colony.BuildShip())
        self.update(self.shipTime)
        
        s1.loadFuel(500)
        s1.loadFuel(20)
        s1.go(self.p3)
        s3 = self.c1.getUnit(1)
        s3.loadFood(100)
        s3.go(self.p2)
        s2.go(self.p3)
        self.update(1)
        self.assertTrue(self.c3.hasUnit(s1))
        self.assertTrue(self.c3.hasUnit(s2))
        self.assertTrue(self.c1.hasUnit(s3))
        self.assertResources(self.c1,0,20,0)
        self.assertResources(self.c2,0,120,100)
        self.assertResources(self.c3,3,20,0)
        
        s3.go(self.p3)
        self.c3.build(colony.BuildDrone())
        self.c3.build(colony.BuildDrone())
        self.c3.build(colony.BuildDrone())
        self.update(self.droneTime*3)
        self.assertTrue(self.c3.hasUnit(s1))
        self.assertTrue(self.c3.hasUnit(s2))
        self.assertTrue(self.c3.hasUnit(s3))
        self.assertResources(self.c1,0,0,0)
        self.assertResources(self.c2,0,120,100)
        self.assertResources(self.c3,0,20,50)
        self.assertEqual(self.c1.production(), 1)
        self.assertEqual(self.c2.production(), 1)
        self.assertEqual(self.c3.production(), 4)
        
        w1 = self.c3.getUnit(3)
        w2 = self.c3.getUnit(4)
        w3 = self.c3.getUnit(5)
        s1.loadUnit(w1)
        s1.loadUnit(w2)
        s2.loadUnit(w3)
        s1.go(self.p2)
        s2.go(self.p2)
        self.update(1)
        self.assertTrue(self.c2.hasUnit(s1))
        self.assertTrue(self.c2.hasUnit(s2))
        self.assertTrue(self.c3.hasUnit(s3))
        self.assertTrue(self.c2.hasUnit(w1))
        self.assertTrue(self.c3.hasUnit(w2))
        self.assertTrue(self.c2.hasUnit(w3))
        self.assertResources(self.c1,0,0,0)
        self.assertResources(self.c2,0,120,100)
        self.assertResources(self.c3,0,0,50)
        self.assertEqual(self.c1.production(), 1)
        self.assertEqual(self.c2.production(), 3)
        self.assertEqual(self.c3.production(), 2)
        
        s1.loadUnit(w1)
        s2.loadFuel(55)
        s1.go(self.p1)
        s2.go(self.p3)
        self.update(1)
        self.assertTrue(self.c1.hasUnit(s1))
        self.assertTrue(self.c3.hasUnit(s2))
        self.assertTrue(self.c3.hasUnit(s3))
        self.assertTrue(self.c1.hasUnit(w1))
        self.assertTrue(self.c3.hasUnit(w2))
        self.assertTrue(self.c2.hasUnit(w3))
        self.assertResources(self.c1,0,0,0)
        self.assertResources(self.c2,0,5,100)
        self.assertResources(self.c3,0,55,50)
        self.assertEqual(self.c1.production(), 2)
        self.assertEqual(self.c2.production(), 2)
        self.assertEqual(self.c3.production(), 2)
        
        s2.loadUnit(s3)
        s2.go(self.p2)
        self.update(1)
        self.assertTrue(self.c1.hasUnit(s1))
        self.assertTrue(self.c2.hasUnit(s2))
        self.assertTrue(self.c3.hasUnit(s3))
        
        s3.loadUnit(w3)
        s3.go(self.p2)
        self.update(1)
        self.assertTrue(self.c1.hasUnit(s1))
        self.assertTrue(self.c2.hasUnit(s2))
        self.assertTrue(self.c2.hasUnit(s3))
        self.assertTrue(self.c1.hasUnit(w1))
        self.assertTrue(self.c3.hasUnit(w2))
        self.assertTrue(self.c2.hasUnit(w3))

if __name__ == '__main__':
    unittest.main()
