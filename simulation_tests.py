import unittest
from simulation import BaseSimulator

#Simulation rules
res_water = "WATER"
res_oxygen = "OXYGEN"
res_food = "FOOD"
res_energy = "ENERGY"

resident_oxygen_demand = 1
resident_water_demand = 2
resident_food_demand = 1

farm_water_demand = 3
farm_energy_demand = 1

farm_food_production = 5
farm_oxygen_production = 2
base_energy_production = 10

class TestBaseSimulator(unittest.TestCase):

    def setUp(self):

        self.initial_resources = {
            res_water: 100,
            res_oxygen: 100,
            res_food: 100,
            res_energy: 100
        }

        self.residents = 3
        self.farms = 1

        self.simulator = BaseSimulator(
            initial_resources=self.initial_resources.copy(),
            residents=self.residents,
            farms=self.farms
        )

    def test_basic_calculations(self):
        #Test 1: Check expected calculations.
        r, f = self.residents, self.farms

        expected_demand = {
            res_oxygen: r * resident_oxygen_demand,
            res_water: (r * resident_water_demand) + (f * farm_water_demand),
            res_food: r * resident_food_demand,
            res_energy: f * farm_energy_demand
        }

        self.assertEqual(self.simulator.calculate(), expected_demand)

    def test_calculate_no_farms(self):
        #Test 2: Check demand with residents but zero farms.
        r, f = 5, 0
        simulator = BaseSimulator(self.initial_resources.copy(), residents=r, farms=f)
        expected_demand = {
            res_oxygen: r * resident_oxygen_demand,
            res_water: (r * resident_water_demand) + (f * farm_water_demand),
            res_food: r * resident_food_demand,
            res_energy: f * farm_energy_demand
        }
        self.assertEqual(simulator.calculate(), expected_demand)

    def test_calculate_no_residents(self):
        #Test 3: Check demand with farms but zero residents.
        r, f = 0, 2
        simulator = BaseSimulator(self.initial_resources.copy(), residents=r, farms=f)
        expected_demand = {
            res_oxygen: r * resident_oxygen_demand,
            res_water: (r * resident_water_demand) + (f * farm_water_demand),
            res_food: r * resident_food_demand,
            res_energy: f * farm_energy_demand
        }
        self.assertEqual(simulator.calculate(), expected_demand)

    def test_calculate_all_zero(self):
        #Test 4: Check demand with zero residents and zero farms.
        simulator = BaseSimulator(self.initial_resources.copy(), residents=0, farms=0)
        expected_demand = {res_oxygen: 0, res_water: 0, res_food: 0, res_energy: 0}
        self.assertEqual(simulator.calculate(), expected_demand)


    def test_consume(self):
        #Test 5: All resources are sufficient.
        demand_amount = 10
        demand = {
            res_oxygen: demand_amount, 
            res_water: demand_amount, 
            res_food: demand_amount, 
            res_energy: demand_amount
        }
        initial_res = self.initial_resources.copy()

        report = self.simulator.consume(demand)
        
        #Check that resources have decreased
        self.assertEqual(self.simulator.resources[res_oxygen], initial_res[res_oxygen] - demand_amount)
        self.assertEqual(self.simulator.resources[res_water], initial_res[res_water] - demand_amount)
        self.assertEqual(self.simulator.resources[res_food], initial_res[res_food] - demand_amount)
        self.assertEqual(self.simulator.resources[res_energy], initial_res[res_energy] - demand_amount)
        
        #Check that the report shows success
        self.assertTrue(report[res_oxygen])
        self.assertTrue(report[res_water])
        self.assertTrue(report[res_food])
        self.assertTrue(report[res_energy])

    def test_consume_multiple(self):
        #Test 6: Both WATER and FOOD are insufficient, but others pass.
        demand_amount = 10
        self.simulator.resources[res_water] = 0
        self.simulator.resources[res_food] = 0

        initial_res = self.simulator.resources.copy()

        demand = {
            res_oxygen: demand_amount, 
            res_water: demand_amount, 
            res_food: demand_amount, 
            res_energy: demand_amount
        }
        report = self.simulator.consume(demand)
        
        #Check that failed resources did not change and report False
        self.assertEqual(self.simulator.resources[res_water], initial_res[res_water])
        self.assertFalse(report[res_water])
        self.assertFalse(report[res_food])
        
        #Check that successful resources were consumed
        self.assertEqual(self.simulator.resources[res_oxygen], initial_res[res_oxygen] - demand_amount)
        self.assertTrue(report[res_oxygen])
        self.assertTrue(report[res_energy])

    def test_consume_insufficient(self):
        #Test 7: Test mixed success/failure at the boundary.
        initial_low_val = 1
        low_resources = {
            res_water: initial_low_val, 
            res_oxygen: initial_low_val, 
            res_food: initial_low_val, 
            res_energy: initial_low_val
        }
        simulator = BaseSimulator(low_resources, residents=1, farms=1)
        demand = simulator.calculate()
        
        report = simulator.consume(demand)
        
        #WATER should fail (need 4, have 1), stock remains 1
        self.assertFalse(report[res_water])
        self.assertEqual(simulator.resources[res_water], initial_low_val)
        
        #Others should succeed (need 1, have 1), stock becomes 0
        self.assertTrue(report[res_oxygen])
        self.assertTrue(report[res_food])
        self.assertTrue(report[res_energy])
        self.assertEqual(simulator.resources[res_oxygen], initial_low_val - demand[res_oxygen])
        self.assertEqual(simulator.resources[res_food], initial_low_val - demand[res_food])

    def test_consume_exact_amount(self):
        #Test 8: Stockpile has the exact amount needed.
        initial_res = self.initial_resources.copy()
        demand = initial_res
        report = self.simulator.consume(demand)
        
        #Resources should be zeroed out
        self.assertEqual(self.simulator.resources[res_oxygen], initial_res[res_oxygen] - demand[res_oxygen])
        self.assertTrue(report[res_oxygen])
        self.assertEqual(self.simulator.resources[res_water], initial_res[res_water] - demand[res_water])
        self.assertTrue(report[res_water])

    def test_produce(self):
        #Test 9: Farms produce (got WATER and ENERGY).
        report = {res_water: True, res_energy: True, res_food: True, res_oxygen: True}
        initial_res = self.initial_resources.copy()
        self.simulator.produce(report)
        
        #Check resource addition
        expected_food = initial_res[res_food] + (self.farms * farm_food_production)
        expected_oxygen = initial_res[res_oxygen] + (self.farms * farm_oxygen_production)
        expected_energy = initial_res[res_energy] + base_energy_production

        self.assertEqual(self.simulator.resources[res_food], expected_food)
        self.assertEqual(self.simulator.resources[res_oxygen], expected_oxygen)
        self.assertEqual(self.simulator.resources[res_energy], expected_energy)

    def test_produce_no_water_or_energy(self):
        #Test 10: Farms do NOT produce (no WATER or ENERGY).
        report = {res_water: False, res_energy: False, res_food: True, res_oxygen: True}
        initial_res = self.initial_resources.copy()
        self.simulator.produce(report)
        
        #Farms should not produce anything (because report["WATER"] and report["ENERGY"] are not both True)
        self.assertEqual(self.simulator.resources[res_food], initial_res[res_food])
        self.assertEqual(self.simulator.resources[res_oxygen], initial_res[res_oxygen])
        #Base energy production always happens
        self.assertEqual(self.simulator.resources[res_energy], initial_res[res_energy] + base_energy_production)
        
    def test_produce_multiple_farms(self):
        #Test 11: Production scales with farm count.
        r, f = 0, 3
        initial_res = self.initial_resources.copy()
        simulator = BaseSimulator(self.initial_resources.copy(), residents=r, farms=f)
        report = {res_water: True, res_energy: True, res_food: True, res_oxygen: True}
        simulator.produce(report)
        
        #Check that production scaled correctly
        self.assertEqual(simulator.resources[res_food], initial_res[res_food] + (f * farm_food_production))
        self.assertEqual(simulator.resources[res_oxygen], initial_res[res_oxygen] + (f * farm_oxygen_production))
        self.assertEqual(simulator.resources[res_energy], initial_res[res_energy] + base_energy_production)

    def test_simulate_one_day_main_scenario(self):
        #Test 12: Integration test for a single day (main scenario).
        r, f = self.residents, self.farms
        initial_res = self.initial_resources.copy()
        self.simulator.simulate()
       
        expected_resources = {
            res_water: initial_res[res_water] - ((r * resident_water_demand) + (f * farm_water_demand)),
            res_oxygen: initial_res[res_oxygen] - (r * resident_oxygen_demand) + (f * farm_oxygen_production),
            res_food: initial_res[res_food] - (r * resident_food_demand) + (f * farm_food_production),
            res_energy: initial_res[res_energy] - (f * farm_energy_demand) + base_energy_production
        }

        self.assertEqual(self.simulator.resources, expected_resources)

    def test_simulate_one_day_farm_failure(self):
        #Test 13: Integration test where farms fail to consume.
        #Set 0 water, so farm production will fail
        r, f = self.residents, self.farms
        self.simulator.resources[res_water] = 0 
        initial_res_modified = self.simulator.resources.copy()
        self.simulator.simulate()
      
        #Check that farm production did not occur
        expected_resources = {
            res_water: initial_res_modified[res_water],
            res_oxygen: initial_res_modified[res_oxygen] - (r * resident_oxygen_demand),
            res_food: initial_res_modified[res_food] - (r * resident_food_demand),
            res_energy: initial_res_modified[res_energy] - (f * farm_energy_demand) + base_energy_production
        }
        self.assertEqual(self.simulator.resources, expected_resources)

    def test_run_simulation_zero_days(self):
        #Test 14: Running for 0 days changes nothing.
        self.simulator.run_simulation(0)
        self.assertEqual(self.simulator.resources, self.initial_resources)

    def test_simulation(self):
        #Test 15: The standart version of solution checked.
        r, f = self.residents, self.farms
        days = 5
        initial_res = self.initial_resources.copy()
        final_resources = self.simulator.run_simulation(days)

        delta_water = -((r * resident_water_demand) + (f * farm_water_demand))
        delta_oxygen = (f * farm_oxygen_production) - (r * resident_oxygen_demand)
        delta_food = (f * farm_food_production) - (r * resident_food_demand)
        delta_energy = base_energy_production - (f * farm_energy_demand)
        
        expected_resources = {
            res_water:   initial_res[res_water] + (delta_water * days),
            res_oxygen:  initial_res[res_oxygen] + (delta_oxygen * days),
            res_food:    initial_res[res_food] + (delta_food * days),
            res_energy:  initial_res[res_energy] + (delta_energy * days)
        }
        self.assertEqual(final_resources, expected_resources)
        
    def test_water_depletes(self):
        #Test 16: Test resource depletion and its effect on production.
        self.simulator.resources[res_water] = 20
        final_resources = self.simulator.run_simulation(3)

        expected_resources = {
            res_water: 2,
            res_oxygen: 95,
            res_food: 101,
            res_energy: 127
        }
        self.assertEqual(final_resources, expected_resources)

    def test_wrong_type(self):
            #Test 17: Test for TypeError with various invalid resource types.
            
            invalid_values = [
                "100",      # string
                None,       # NoneType
                [100],      # list
                {"val": 100}, # dict
                (100,)      # tuple
            ]
            
            for invalid_value in invalid_values:
                with self.subTest(value=invalid_value, type=type(invalid_value)):
                    wrong_type_resources = {
                        res_water: 100,
                        res_oxygen: invalid_value,
                        res_food: 100,
                        res_energy: 100
                    }
                    
                    simulator = BaseSimulator(wrong_type_resources, residents=1, farms=0)
                    
                    with self.assertRaises(TypeError):
                        simulator.simulate()

if __name__ == "__main__":
    unittest.main()