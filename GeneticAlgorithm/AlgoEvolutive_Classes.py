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
    def __init__(self, chromosome, mutation_rate):
        self.chromosome = chromosome
        self.fitness = 0
        self.mutation_rate = mutation_rate

    def __str__(self):
        return f"Individual: {self.chromosome} Fitness: {self.fitness}"

    def __repr__(self):
        return self.__str__()


class population:
    def __init__(self, gene_pool, population_size, fitness_function, crossover_rate=0.0, mutation_rate=0.0):
        self.cross_over_rate = crossover_rate

        self.individuals = []
        for i in range(population_size):
            chromosome = gene_pool.copy()
            np.random.shuffle(chromosome)
            self.individuals.append(individual(chromosome, mutation_rate))

        self.fitness_function = fitness_function
        self.best_individual = None

    def __str__(self):
        return "\n".join([str(individual) for individual in self.individuals]) + f"\nBest individual: {self.best_individual}\n"

    def fitness_evaluation(self, *args):
        fitness_each_individual = self.fitness_function(self.individuals, *args)
        for individual in self.individuals:
            individual.fitness = fitness_each_individual.pop(0)

        self.best_individual = min(self.individuals, key=lambda individual: individual.fitness)

    def selection(self, amount_of_survivors):
        self.individuals = sorted(self.individuals, key=lambda individual: individual.fitness)
        self.individuals = self.individuals[:amount_of_survivors]

    def create_offspring(self, parent_a, parent_b):
        chromosome_a = parent_a.chromosome
        chromosome_b = parent_b.chromosome

        offspring_chromosome = []
        # start = random.randint(0, len(parent_a) - 1)
        start = np.random.randint(0, len(chromosome_a) - 1)
        # finish = random.randint(start, len(parent_a))
        finish = np.random.randint(start, len(chromosome_a))
        sub_path_from_a = chromosome_a[start:finish]
        remaining_path_from_b = list([item for item in chromosome_b if item not in sub_path_from_a])
        for i in range(0, len(chromosome_a)):
            if start <= i < finish:
                offspring_chromosome.append(sub_path_from_a.pop(0))
            else:
                offspring_chromosome.append(remaining_path_from_b.pop(0))
        return offspring_chromosome

    def crossover(self):
        offsprings = []
        midway = len(self.individuals) // 2
        for i in range(midway):
            if np.random.randint(0, 1) < self.cross_over_rate:
                parent_a, parent_b = self.individuals[i], self.individuals[i + midway]
                for _ in range(2):
                    offsprings.append(individual(self.create_offspring(parent_a, parent_b), parent_a.mutation_rate))
                    offsprings.append(individual(self.create_offspring(parent_b, parent_a), parent_b.mutation_rate))

        self.individuals = offsprings

    def mutate(self):
        gen_wt_mutations = []
        for individual in self.individuals:
            path = individual.chromosome
            if np.random.randint(0, 100) < individual.mutation_rate:
                index1, index2 = np.random.randint(1, len(path) - 1), np.random.randint(1, len(path) - 1)
                path[index1], path[index2] = path[index2], path[index1]
            gen_wt_mutations.append(path)

    def evolve(self, *args):
        self.selection(len(self.individuals) // 2)
        self.crossover()
        self.mutate()
        self.fitness_evaluation(*args)