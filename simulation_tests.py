import unittest
from simulation import BaseSimulator

class TestBaseSimulator(unittest.TestCase):

    def setUp(self):

        self.initial_resources = {
            "WATER": 100,
            "OXYGEN": 100,
            "FOOD": 100,
            "ENERGY": 100
        }
        self.simulator = BaseSimulator(
            initial_resources=self.initial_resources.copy(),
            residents=3,
            farms=1
        )

    def test_basic_calculations(self):
        #Test 1: Check expected calculations.
        expected_demand = {
            "OXYGEN": 3,
            "WATER": 9,
            "FOOD": 3,
            "ENERGY": 1
        }
        self.assertEqual(self.simulator._calculate(), expected_demand)

    def test_calculate_no_farms(self):
        #Test 2: Check demand with residents but zero farms.
        simulator = BaseSimulator(self.initial_resources.copy(), residents=5, farms=0)
        expected_demand = {
            "OXYGEN": 5,
            "WATER": 10,
            "FOOD": 5,
            "ENERGY": 0 
        }
        self.assertEqual(simulator._calculate(), expected_demand)

    def test_calculate_no_residents(self):
        #Test 3: Check demand with farms but zero residents.
        simulator = BaseSimulator(self.initial_resources.copy(), residents=0, farms=2)
        expected_demand = {
            "OXYGEN": 0,
            "WATER": 6,
            "FOOD": 0,
            "ENERGY": 2 
        }
        self.assertEqual(simulator._calculate(), expected_demand)

    def test_calculate_all_zero(self):
        #Test 4: Check demand with zero residents and zero farms.
        simulator = BaseSimulator(self.initial_resources.copy(), residents=0, farms=0)
        expected_demand = {"OXYGEN": 0, "WATER": 0, "FOOD": 0, "ENERGY": 0}
        self.assertEqual(simulator._calculate(), expected_demand)


    def test_consume(self):
        #Test 5: All resources are sufficient.
        demand = {"OXYGEN": 10, "WATER": 10, "FOOD": 10, "ENERGY": 10}
        report = self.simulator._consume(demand)
        
        self.assertEqual(self.simulator.resources["OXYGEN"], 90)
        self.assertEqual(self.simulator.resources["WATER"], 90)
        self.assertEqual(self.simulator.resources["FOOD"], 90)
        self.assertEqual(self.simulator.resources["ENERGY"], 90)
        
        self.assertTrue(report["OXYGEN"])
        self.assertTrue(report["WATER"])
        self.assertTrue(report["FOOD"])
        self.assertTrue(report["ENERGY"])

    def test_consume_multiple(self):
        #Test 6: Both WATER and FOOD are insufficient, but others pass.
        self.simulator.resources["WATER"] = 0
        self.simulator.resources["FOOD"] = 0
        demand = {"OXYGEN": 10, "WATER": 10, "FOOD": 10, "ENERGY": 10}
        report = self.simulator._consume(demand)
        
        self.assertEqual(self.simulator.resources["WATER"], 0)
        self.assertFalse(report["WATER"])
        self.assertEqual(self.simulator.resources["FOOD"], 0)
        self.assertFalse(report["FOOD"])
        
        self.assertEqual(self.simulator.resources["OXYGEN"], 90)
        self.assertTrue(report["OXYGEN"])
        self.assertEqual(self.simulator.resources["ENERGY"], 90)
        self.assertTrue(report["ENERGY"])

    def test_consume_insufficient(self):
        #Test 7: Test mixed success/failure at the boundary.
        low_resources = {"WATER": 1, "OXYGEN": 1, "FOOD": 1, "ENERGY": 1}
        simulator = BaseSimulator(low_resources, residents=1, farms=1)
        demand = simulator._calculate()
        
        report = simulator._consume(demand)
        
        self.assertFalse(report["WATER"])
        self.assertEqual(simulator.resources["WATER"], 1)
        
        self.assertTrue(report["OXYGEN"])
        self.assertTrue(report["FOOD"])
        self.assertTrue(report["ENERGY"])
        self.assertEqual(simulator.resources["OXYGEN"], 0)
        self.assertEqual(simulator.resources["FOOD"], 0)

    def test_consume_exact_amount(self):
        #Test 8: Stockpile has the exact amount needed.
        demand = {"OXYGEN": 100, "WATER": 100, "FOOD": 100, "ENERGY": 100}
        report = self.simulator._consume(demand)
        
        self.assertEqual(self.simulator.resources["OXYGEN"], 0)
        self.assertTrue(report["OXYGEN"])
        self.assertEqual(self.simulator.resources["WATER"], 0)
        self.assertTrue(report["WATER"])

    def test_produce(self):
        #Test 9: Farms produce (got WATER and ENERGY).
        report = {"WATER": True, "ENERGY": True, "FOOD": True, "OXYGEN": True}
        self.simulator._produce(report)
        
        self.assertEqual(self.simulator.resources["FOOD"], 105)
        self.assertEqual(self.simulator.resources["OXYGEN"], 102)
        self.assertEqual(self.simulator.resources["ENERGY"], 110)

    def test_produce_no_water_or_energy(self):
        #Test 10: Farms do NOT produce (no WATER or ENERGY).
        report = {"WATER": False, "ENERGY": False, "FOOD": True, "OXYGEN": True}
        self.simulator._produce(report)
        
        self.assertEqual(self.simulator.resources["FOOD"], 100)
        self.assertEqual(self.simulator.resources["OXYGEN"], 100)
        self.assertEqual(self.simulator.resources["ENERGY"], 110)
        
    def test_produce_multiple_farms(self):
        #Test 11: Production scales with farm count.
        simulator = BaseSimulator(self.initial_resources.copy(), residents=0, farms=3)
        report = {"WATER": True, "ENERGY": True, "FOOD": True, "OXYGEN": True}
        simulator._produce(report)
        
        self.assertEqual(simulator.resources["FOOD"], 115)
        self.assertEqual(simulator.resources["OXYGEN"], 106)
        self.assertEqual(simulator.resources["ENERGY"], 110)

if __name__ == "__main__":
    unittest.main()