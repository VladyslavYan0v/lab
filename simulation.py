class BaseSimulator:
  
    def __init__(self, initial_resources: dict, residents: int, farms: int):
        self.resources = initial_resources
        self.residents = residents
        self.farms = farms

    # calculation of resources used in one day
    def calculate(self) -> dict:
        consumption = {
            "OXYGEN": self.residents * 1,
            "WATER": (self.residents * 2) + (self.farms * 3),
            "FOOD": self.residents * 1,
            "ENERGY": self.farms * 1,
        }
        return consumption

    # applying changes in resources
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

    # calculation of resources produced in one day
    def produce(self, consumption_report: dict) -> None:
        if consumption_report["WATER"] and consumption_report["ENERGY"]:
            self.resources["FOOD"] += self.farms * 5
            self.resources["OXYGEN"] += self.farms * 2
            
        self.resources["ENERGY"] += 10

    # simulation of one day
    def simulate(self) -> None:
        consumption = self.calculate()
        
        report = self.consume(consumption)
        
        self.produce(report)

    # simulation of the period of days
    def run_simulation(self, days: int) -> dict:
        for _ in range(days):
            self.simulate()
        return self.resources
