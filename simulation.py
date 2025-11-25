##
# @brief Class for colony resource management simulation.
#
# This class manages the consumption (calculate, consume) and production (produce)
# of resources based on the number of residents and farms.
class BaseSimulator:
    ##
    # @brief Initializes the simulator.
    #
    # @param initial_resources Dictionary of initial resources (OXYGEN, WATER, FOOD, ENERGY).
    # @param residents Number of residents in the colony.
    # @param farms Number of farms in the colony.
    
  
    def __init__(self, initial_resources: dict, residents: int, farms: int):
        self.resources = initial_resources
        self.residents = residents
        self.farms = farms

    ##
    # @brief Calculates resources required for one day.
    #
    # @return Dict[str, int] A dictionary containing the calculated demand for each resource.
    def calculate(self) -> dict:
        consumption = {
            "OXYGEN": self.residents * 1,
            "WATER": (self.residents * 2) + (self.farms * 3),
            "FOOD": self.residents * 1,
            "ENERGY": self.farms * 1,
        }
        return consumption

    ##
    # @brief Applies resource consumption changes.
    #
    # Checks if there are enough resources in storage.
    #
    # @param consumption Dictionary of required resources.
    # @return Dict[str, bool] Report indicating which resources were successfully consumed.
    def consume(self, consumption: dict) -> dict:
        report = {"WATER": False, "ENERGY": False, "FOOD": False, "OXYGEN": False}

        can_consume_oxygen = self.resources["OXYGEN"] >= consumption["OXYGEN"]
        can_consume_water = self.resources["WATER"] >= consumption["WATER"]
        can_consume_food = self.resources["FOOD"] >= consumption["FOOD"]
        can_consume_energy = self.resources["ENERGY"] >= consumption["ENERGY"]

        if can_consume_oxygen:
            self.resources["OXYGEN"] -= consumption["OXYGEN"]
            report["OXYGEN"] = True
            
        if can_consume_water:
            self.resources["WATER"] -= consumption["WATER"]
            report["WATER"] = True

        if can_consume_food:
            self.resources["FOOD"] -= consumption["FOOD"]
            report["FOOD"] = True

        if can_consume_energy:
            self.resources["ENERGY"] -= consumption["ENERGY"]
            report["ENERGY"] = True
            
        return report

    ##
    # @brief Calculates produced resources for one day.
    #
    # If WATER and ENERGY were successfully consumed, farms produce FOOD and OXYGEN.
    # ENERGY is always produced.
    #
    # @param consumption_report Report indicating if resources were allocated for production.
    def produce(self, consumption_report: dict) -> None:
        if consumption_report["WATER"] and consumption_report["ENERGY"]:
            self.resources["FOOD"] += self.farms * 5
            self.resources["OXYGEN"] += self.farms * 2
            
        self.resources["ENERGY"] += 10

    ##
    # @brief Simulates a single day cycle.
    def simulate(self) -> None:
        consumption = self.calculate()
        
        report = self.consume(consumption)
        
        self.produce(report)

    ##
    # @brief Runs the simulation for a specific number of days.
    #
    # @param days Number of days to simulate.
    # @return Dict[str, int] Final state of resources.
    def run_simulation(self, days: int) -> dict:
        for _ in range(days):
            self.simulate()
        return self.resources
