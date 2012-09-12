import unittest
import planet
import colony
import units
import buildings
import math

class TestColony(unittest.TestCase):
    def setUp(self):
        self.fuelRate = 10
        self.fuelTime = 10
        self.mineTime = 10
        self.manufactoryTime = 10
        self.reclaimTime = 10
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
        for i in range(0,math.ceil(turns)):
            self.c1.update()
            self.c2.update()
            self.c3.update()
    
    def test_fuel(self):
        self.c1.build(colony.BuildBuilding(buildings.FuelExtractor))
        self.c2.build(colony.BuildBuilding(buildings.FuelExtractor))
        self.c3.build(colony.BuildBuilding(buildings.FuelExtractor))
        self.update(self.fuelTime)
        self.update(20)
        self.assertEqual(self.c1.fuel, 0)
        self.assertEqual(self.c1.fuel + self.c1.planet.fuel, self.initial[self.c1]['fuel'])
        self.assertEqual(self.c2.fuel, 20*self.fuelRate)
        self.assertEqual(self.c2.fuel + self.c2.planet.fuel, self.initial[self.c2]['fuel'])
        self.assertEqual(self.c3.fuel, 0)
        self.assertEqual(self.c3.fuel + self.c3.planet.fuel, self.initial[self.c3]['fuel'])
        self.update(500/self.fuelRate)
        self.assertEqual(self.c1.fuel, 0)
        self.assertEqual(self.c1.fuel + self.c1.planet.fuel, self.initial[self.c1]['fuel'])
        self.assertEqual(self.c2.fuel, 500)
        self.assertEqual(self.c2.fuel + self.c2.planet.fuel, self.initial[self.c2]['fuel'])
        self.assertEqual(self.c3.fuel, 0)
        self.assertEqual(self.c3.fuel + self.c3.planet.fuel, self.initial[self.c3]['fuel'])

    def test_metal(self):
        self.c1.build(colony.BuildMine())
        self.c2.build(colony.BuildMine())
        self.c3.build(colony.BuildMine())
        self.update(self.mineTime)
        self.assertEqual(self.c1.metal, 1)
        self.assertEqual(self.c1.metal + self.c1.planet.metal, self.initial[self.c1]['metal'])
        self.assertEqual(self.c2.metal, 0)
        self.assertEqual(self.c2.metal + self.c2.planet.metal, self.initial[self.c2]['metal'])
        self.assertEqual(self.c3.metal, 0)
        self.assertEqual(self.c3.metal + self.c3.planet.metal, self.initial[self.c3]['metal'])
        for i in range(0,5):
            self.c1.build(colony.BuildMine())
            self.c2.build(colony.BuildMine())
            self.c3.build(colony.BuildMine())
        self.update(5*self.mineTime)
        self.assertEqual(self.c1.metal, 5)
        self.assertEqual(self.c1.metal + self.c1.planet.metal, self.initial[self.c1]['metal'])
        self.assertEqual(self.c2.metal, 0)
        self.assertEqual(self.c2.metal + self.c2.planet.metal, self.initial[self.c2]['metal'])
        self.assertEqual(self.c3.metal, 0)
        self.assertEqual(self.c3.metal + self.c3.planet.metal, self.initial[self.c3]['metal'])
    
    def test_drone(self):
        self.c1.build(colony.BuildMine())
        self.c2.build(colony.BuildMine())
        self.c3.build(colony.BuildMine())
        self.c1.build(colony.BuildMine())
        self.c2.build(colony.BuildMine())
        self.c3.build(colony.BuildMine())
        self.update(self.mineTime*2)
        self.assertEqual(self.c1.metal, 2)
        self.assertEqual(self.c2.metal, 0)
        self.assertEqual(self.c3.metal, 0)
        self.c1.metal += 2
        self.c2.metal += 2
        self.c3.metal += 2
        self.c1.build(colony.BuildBuilding(buildings.Manufactory))
        self.c2.build(colony.BuildBuilding(buildings.Manufactory))
        self.c3.build(colony.BuildBuilding(buildings.Manufactory))
        self.update(self.manufactoryTime)
        self.assertEqual(self.c1.metal, 2)
        self.assertEqual(self.c2.metal, 0)
        self.assertEqual(self.c3.metal, 0)
        m1 = self.c1.getBuildings(buildings.Manufactory)[0]
        m2 = self.c2.getBuildings(buildings.Manufactory)[0]
        m3 = self.c3.getBuildings(buildings.Manufactory)[0]
        for i in range(0,3):
            m1.construct(units.Drone)
            m2.construct(units.Drone)
            m3.construct(units.Drone)
        self.update(self.droneTime)
        self.assertEqual(self.c1.production(),2)
        self.assertEqual(self.c2.production(),1)
        self.assertEqual(self.c3.production(),1)
        self.update(self.droneTime*2)
        self.assertEqual(self.c1.production(),3)
        self.assertEqual(self.c2.production(),1)
        self.assertEqual(self.c3.production(),1)
    
    def test_reclaim(self):
        for i in range(0,5):
            self.c1.build(colony.BuildMine())
            self.update(self.mineTime)
        self.assertEqual(self.c1.metal, 5)
        self.c1.build(colony.BuildBuilding(buildings.Manufactory))
        self.c1.build(colony.BuildBuilding(buildings.ReclamationFacility))
        self.c2.metal += 1
        self.c2.build(colony.BuildBuilding(buildings.ReclamationFacility))
        self.update(self.manufactoryTime+self.reclaimTime)
        m1 = self.c1.getBuildings(buildings.Manufactory)[0]
        r1 = self.c1.getBuildings(buildings.ReclamationFacility)[0]
        r2 = self.c2.getBuildings(buildings.ReclamationFacility)[0]
        self.assertEqual(self.c1.metal, 2)
        m1.construct(units.Drone)
        m1.construct(units.Drone)
        self.update(self.droneTime*2)
        d1 = self.c1.getUnit(0)
        d2 = self.c1.getUnit(1)
        self.assertEqual(self.c1.metal, 0)
        self.assertEqual(self.c2.metal, 0)
        r1.reclaim(d1)
        self.assertEqual(self.c1.metal, 1)
        self.assertEqual(self.c2.metal, 0)
        r2.reclaim(d1)
        self.assertEqual(self.c1.metal, 1)
        self.assertEqual(self.c2.metal, 0)
        r2.reclaim(d2)
        self.assertEqual(self.c1.metal, 1)
        self.assertEqual(self.c2.metal, 0)
        r1.reclaim(d1)
        self.assertEqual(self.c1.metal, 1)
        self.assertEqual(self.c2.metal, 0)
        r1.reclaim(d2)
        self.assertEqual(self.c1.metal, 2)
        self.assertEqual(self.c2.metal, 0)
        
        

class TestShip(unittest.TestCase):
    def setUp(self):
        self.shipTime = 10
        self.droneTime = 10
        self.manufactoryTime = 10
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
        self.c1.metal += 2
        self.c2.metal += 2
        self.c3.metal += 2
        self.c1.build(colony.BuildBuilding(buildings.Manufactory))
        self.c2.build(colony.BuildBuilding(buildings.Manufactory))
        self.c3.build(colony.BuildBuilding(buildings.Manufactory))
        self.update(self.manufactoryTime)
        m1 = self.c1.getBuildings(buildings.Manufactory)[0]
        m2 = self.c2.getBuildings(buildings.Manufactory)[0]
        m3 = self.c3.getBuildings(buildings.Manufactory)[0]

        m1.construct(units.Ship)
        m1.construct(units.Ship)
        m2.construct(units.Ship)
        m3.construct(units.Ship)
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
        
        m1.construct(units.Ship)
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
        m3.construct(units.Drone)
        m3.construct(units.Drone)
        m3.construct(units.Drone)
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
