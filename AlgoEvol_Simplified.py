# Traveler's problem - Evolutive algorithm approach
import os
import numpy as np


# Load file
def load_file(file_name):
    file = open(file_name, "r")
    data = file.readlines()
    file.close()
    return data


data = load_file("./Evol/DatosSimple.txt")

# Read number of labels
n = int(data[0])

# Read labels
labels = []
for i in range(1, n + 1):
    labels.append(data[i].strip())

# Read distances
distances_matrix = []
for i in range(n + 1, n + 1 + n):
    distances_matrix.append(list(map(int, data[i].strip().split())))

distances_matrix = np.array(distances_matrix)

# Dict to translate labels to indexes
labels_dict = {label: i for i, label in enumerate(labels)}

print(f"Number of points: {n} \nLabels: {labels} \nDistances: \n{distances_matrix}")

# Read labels to visit
m = int(data[n + 1 + n])
labels_to_visit = []

for i in range(n + 2 + n, n + 2 + n + m):
    labels_to_visit.append(data[i].strip())

print(f"\nPoints to visit: {labels_to_visit}")

population_size = int(data[n + 2 + n + m])  # Read number of individuals in the population
generations = int(data[n + 3 + n + m])  # Read number of generations
crossover_rate = float(data[n + 4 + n + m])  # Crossover rate
mutation_rate = float(data[n + 5 + n + m])  # Mutation rate

print(
    f"\nPopulation size: {population_size} \nGenerations: {generations} \nInversion rate: {crossover_rate} \nMutation rate: {mutation_rate}")


# Initialize random population, by shuffling the labels to visit but keeping the first element fixed
def initialize_population():
    population = []
    for i in range(population_size):
        individual = labels_to_visit.copy()
        np.random.shuffle(individual)

        # Keep the first element fixed
        for i in range(1, len(individual)):
            if individual[i] == labels_to_visit[0]:
                individual[i], individual[0] = individual[0], individual[i]
                break

        population.append(individual)

    return np.array(population)


random_population = initialize_population()

print(f"\nRandom population: {random_population}")


# Evolution

# Calculate the total distance of an individual
def total_distance(individual, distances):
    total = 0
    for i in range(len(individual) - 1):
        total += distances[labels_dict[individual[i]]][labels_dict[individual[i + 1]]]
    total += distances[labels_dict[individual[-1]]][labels_dict[individual[0]]]
    return total


distances_random_population = [total_distance(individual, distances_matrix) for individual in random_population]
print(f"\nTotal distance of random population: {distances_random_population}")

# Select only the half of the best individuals in the previous generation
def selection(population, distances):
    best_individuals = []
    for individual in population:
        best_individuals.append((individual, total_distance(individual, distances)))

    best_individuals.sort(key=lambda x: x[1])

    return np.array([individual for individual, _ in best_individuals[:population_size // 2]])

best_individuals = selection(random_population, distances_matrix)
print(f"\nBest individuals: {best_individuals}")
