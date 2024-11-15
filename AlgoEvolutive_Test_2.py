from os import system
import time
import numpy as np
from GeneticAlgorithm.AlgoEvolutive_Classes import individual, population


# Custom fitness functions
def total_distance(individuals, distances, labels_dict):
    for individual in individuals:
        total = distances[labels_dict["Madrid"]][labels_dict[individual.chromosome[0]]]
        for i in range(len(individual.chromosome) - 1):
            #total += distances[individual.chromosome[i]][individual.chromosome[i + 1]]
            total += distances[labels_dict[individual.chromosome[i]]][labels_dict[individual.chromosome[i + 1]]]

        # Circle back to the first element
        #total += distances[individual.chromosome[-1]][individual.chromosome[0]]
        total += distances[labels_dict[individual.chromosome[-1]]][labels_dict["Madrid"]]
        individual.fitness = total
    return [individual.fitness for individual in individuals]


# Load file
def load_file(file_name):
    file = open(file_name, "r")
    data = file.readlines()
    file.close()
    return data


data = load_file("./Evol/Datos2.txt")

n = int(data[0])                                            # Read number of labels

# Read labels
labels = []
for i in range(1, n + 1):
    labels.append(data[i].strip())

# Read distances
distances_matrix = []
for i in range(n + 1, n + 1 + n):
    distances_matrix.append(list(map(int, data[i].strip().split())))

distances_matrix = np.array(distances_matrix)

labels_dict = {label: i for i, label in enumerate(labels)}  # Dict to translate labels to indexes

print(f"Number of points: {n} \nLabels: {labels} \nDistances: \n{distances_matrix}")

# Read labels to visit
m = int(data[n + 1 + n])
labels_to_visit = []
for i in range(n + 2 + n, n + 2 + n + m):
    labels_to_visit.append(data[i].strip())

print(f"\nPoints to visit: {labels_to_visit}")

population_size = int(data[n + 2 + n + m])      # Read number of individuals in the population
generations = int(data[n + 3 + n + m])          # Read number of generations
crossover_rate = float(data[n + 4 + n + m])     # Crossover rate
mutation_rate = float(data[n + 5 + n + m])      # Mutation rate


# Initialize population
poblacion = population(labels_to_visit, population_size, total_distance, mutation_rate=35, crossover_rate=80)
poblacion.fitness_evaluation(distances_matrix, labels_dict)

print(poblacion)

# Continue evolving
while True:
    poblacion.evolve(distances_matrix, labels_dict)
    print(poblacion.best_individual)

