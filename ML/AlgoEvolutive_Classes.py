from os import system
import time
import numpy as np

# The basic flow of a genetic algorithm is as follows:
# 1. Initialize the population (generation zero)
# 2. Evaluate the population (calculate the fitness of each individual)
# Loop begins here
# 3. Select the best individuals according to their fitness
# 4. Create new individuals by crossover
# 5. Mutate
# 6. Evaluate the new population
# Do we have a solution?
# Yes -> Choose the best individuals from the last population
# No -> Loop again


class individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = 0
        # Would cross over and mutation rate for the individual be ideal?

    def __str__(self):
        return f"Individual: {self.chromosome} Fitness: {self.fitness}"


class population:
    def __init__(self, individuals):
        self.individuals = individuals

    def __str__(self):
        return "\n".join([str(individual) for individual in self.individuals])