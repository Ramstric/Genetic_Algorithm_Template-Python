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


class Individual:
    def __init__(self, chromosome, mutation_rate):
        self.chromosome = chromosome
        self.fitness = 0
        self.mutation_rate = mutation_rate

    # Método auxiliar para poder imprimir en consola al Individuo
    #   i.e. print(Individuo)
    def __str__(self):
        return f"\nFitness: {self.fitness} - Individual: {self.chromosome}"

    # Método auxiliar para pdoer imprimir una lista de Individuos
    #   i.e. print( [Individuo_1, Individuo_2, Individuo_3, ...] )
    def __repr__(self):
        return self.__str__()


class Population:
    def __init__(self, gene_pool, population_size, fitness_function, crossover_rate=0.0, mutation_rate=0.0):
        self.individuals = []

        # Initialize a random population
        for i in range(population_size):
            chromosome = gene_pool.copy()
            np.random.shuffle(chromosome)
            self.individuals.append(Individual(chromosome, mutation_rate))

        self.generations = 0
        self.cross_over_rate = crossover_rate

        self.fitness_function = fitness_function
        self.best_individual = None

        self.show_population = True

    # Método auxiliar para poder imprimir en consola la Poblacion
    #   i.e. print(Population)
    def __str__(self):
        if self.show_population:
            return "\nGenerations: " + str(self.generations) + "".join([str(individual) for individual in self.individuals]) + f"\n\nBest individual: {self.best_individual}\n"
        else:
            return f"\nGeneration {self.generations} best individual {self.best_individual}\n"

    def fitness_evaluation(self, *args):

        # Evaluar a cada individuo con los parámetros adicionales '*args'
        for individual in self.individuals:
            individual.fitness = self.fitness_function(individual.chromosome, *args)

        # Ordenar a los individuos en base al puntaje de optimización, de menor a mayor.
        self.individuals = sorted(self.individuals, key=lambda individual: individual.fitness)

        # Encontrar al individuo con el mejor puntaje de optimización
        self.best_individual = self.individuals[0]

    def selection(self, amount_of_survivors, *args):
        self.fitness_evaluation(*args)

        # Seleccionar hasta n Individuos según indique 'amount_of_survivors'
        self.individuals = self.individuals[:amount_of_survivors]

    def crossover_method_basic(self, parent_a, parent_b):
        chromosome_a = parent_a.chromosome
        chromosome_b = parent_b.chromosome

        offspring_chromosome = []

        start = np.random.randint(0, len(chromosome_a) - 1)
        finish = np.random.randint(start, len(chromosome_a))

        sub_path_from_a = chromosome_a[start:finish]
        remaining_path_from_b = list([item for item in chromosome_b if item not in sub_path_from_a])

        for i in range(0, len(chromosome_a)):
            if start <= i < finish:
                offspring_chromosome.append(sub_path_from_a.pop(0))
            else:
                offspring_chromosome.append(remaining_path_from_b.pop(0))

        return Individual(offspring_chromosome, parent_a.mutation_rate)

    def crossover_method_PMX(self, parent_a, parent_b):
        # Primero se recortan los cromosomas de los padres
        chromosome_a = parent_a.chromosome
        chromosome_b = parent_b.chromosome

        start = np.random.randint(0, len(chromosome_a) - 2)
        finish = np.random.randint(start + 1, len(chromosome_a))

        offspring_a = [chromosome_a[:start], chromosome_b[start:finish], chromosome_a[finish:]]
        offspring_b = [chromosome_b[:start], chromosome_a[start:finish], chromosome_b[finish:]]

        # Para legalizar los cromosomas de los hijos...

        # Primero se hace un hashmap de los valores centrales de los cromosomas
        recursive_search_dict = dict()
        for i in range(len(offspring_a[1])):
            recursive_search_dict[offspring_a[1][i]] = offspring_b[1][i]

        # Con una busqueda recursiva, se arregla el hashmap
        mapping_dict_1 = dict()
        mapping_dict_2 = dict()

        for key in recursive_search_dict:
            if key == recursive_search_dict[key]:
                continue

            if key in offspring_a[0] or key in offspring_a[2]:
                start_key = key
                end_key = recursive_search(start_key, recursive_search_dict)
                mapping_dict_1[end_key] = start_key
                mapping_dict_2[start_key] = end_key

        # Se remplazan las variables en los extremos de los cromosomas
        for i in range(len(offspring_a[0])):
            if offspring_a[0][i] in mapping_dict_2:
                offspring_a[0][i] = mapping_dict_2[offspring_a[0][i]]
            if offspring_b[0][i] in mapping_dict_1:
                offspring_b[0][i] = mapping_dict_1[offspring_b[0][i]]

        for i in range(len(offspring_a[2])):
            if offspring_a[2][i] in mapping_dict_2:
                offspring_a[2][i] = mapping_dict_2[offspring_a[2][i]]
            if offspring_b[2][i] in mapping_dict_1:
                offspring_b[2][i] = mapping_dict_1[offspring_b[2][i]]

        # Se unen los cromosomas recortados
        offspring_a = [item for sublist in offspring_a for item in sublist]
        offspring_b = [item for sublist in offspring_b for item in sublist]

        return Individual(offspring_a, parent_a.mutation_rate), Individual(offspring_b, parent_b.mutation_rate)

    def crossover(self):
        offsprings = []
        midway = len(self.individuals) // 2

        for i in range(midway):
            if np.random.randint(0, 100) < self.cross_over_rate:
                parent_a, parent_b = self.individuals[i], self.individuals[i + midway]

                offsprings.extend(self.crossover_method_PMX(parent_a, parent_b))

        self.individuals.extend(offsprings)

    def mutate(self):
        for i in range(1, len(self.individuals)):

            path = self.individuals[i].chromosome

            if np.random.randint(0, 100) < self.individuals[i].mutation_rate:
                index1, index2 = np.random.randint(0, len(path)), np.random.randint(0, len(path))
                self.individuals[i].chromosome[index1], self.individuals[i].chromosome[index2] = self.individuals[i].chromosome[index2], self.individuals[i].chromosome[index1]

    def evolve(self, *args):
        self.generations += 1
        self.selection(len(self.individuals) // 2, *args)
        self.crossover()
        self.mutate()
        self.fitness_evaluation(*args)


def recursive_search(key, mapping_dict):
    if key in mapping_dict:
        return recursive_search(mapping_dict[key], mapping_dict)
    return key
