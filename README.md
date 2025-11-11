Base Ecosystem Simulator
This repository contains a Python class, BaseSimulator, which models and calculates resource changes in a closed base ecosystem. The simulation runs in discrete daily "ticks," applying a fixed set of rules for consumption and production.

The core logic is intended to be used as a "System Under Test".

Project Goal: Unit Testing
The primary objective of this project is  to write a unit test suite for the BaseSimulator logic.

How It Works: The Simulation Rules
The simulation is driven by the BaseSimulator class. When simulate() is called, it executes three distinct phases in order:

First, the system calculates the total required demand for all resources for the day based on the number of residents and farms.

Each Resident requires:

    1 OXYGEN

    2 WATER

    1 FOOD

Each Farm requires:

    3 WATER

    1 ENERGY

Next, the system attempts to fulfill the demand from the available resource stockpile.

If the stockpile has enough of a resource (e.g., WATER) to meet the total demand, the resources are consumed, and the stockpile is reduced.

If the stockpile has insufficient WATER, no WATER is consumed at all by any resident or farm.

This method returns a report dictionary (e.g., {"WATER": True, "ENERGY": False, ...}) indicating which resources were successfully consumed.

Finally, resources are produced based on the success report from Phase 2.

Base Solar Panels:

Always produce 10 ENERGY. This is unconditional.

Hydroponic Farm(s):

Farms produce resources only if their demands for both WATER and ENERGY were successfully met in Phase 2.

If this condition is met, each farm produces:

    5 FOOD

    2 OXYGEN