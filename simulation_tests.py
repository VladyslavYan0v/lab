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

if __name__ == "__main__":
    unittest.main()