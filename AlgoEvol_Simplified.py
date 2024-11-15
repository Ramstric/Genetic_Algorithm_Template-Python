# Traveler's problem - Evolutive algorithm approach
from os import system
import time
import numpy as np


# Load file
def load_file(file_name):
    file = open(file_name, "r")
    data = file.readlines()
    file.close()
    return data


data = load_file("./Evol/Datos3.txt")

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

        # Keep the first element fixed and add it to the end to make the path circular
        for i in range(1, len(individual)):
            if individual[i] == labels_to_visit[0]:
                individual[i], individual[0] = individual[0], individual[i]
                break

        population.append(individual)

    return np.array(population)


random_population = initialize_population()

print(f"\nRandom population: \n{random_population}")


# Evolution

# Calculate the total distance of an individual circling back to the first element
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
print(f"\nBest individuals: \n{best_individuals}")

# Crossover two individuals

def create_offspring(parent_a, parent_b):
    offspring = []
    #start = random.randint(0, len(parent_a) - 1)
    start = np.random.randint(0, len(parent_a) - 1)
    #finish = random.randint(start, len(parent_a))
    finish = np.random.randint(start, len(parent_a))
    sub_path_from_a = parent_a[start:finish]
    remaining_path_from_b = list([item for item in parent_b if item not in sub_path_from_a])
    for i in range(0, len(parent_a)):
        if start <= i < finish:
            offspring.append(sub_path_from_a.pop(0))
        else:
            offspring.append(remaining_path_from_b.pop(0))
    return offspring


def apply_crossovers(survivors):
    offsprings = []
    survivors = [individual.tolist() for individual in survivors]
    midway = len(survivors) // 2
    for i in range(midway):
        parent_a, parent_b = survivors[i], survivors[i + midway]
        for _ in range(2):
            offsprings.append(create_offspring(parent_a, parent_b))
            offsprings.append(create_offspring(parent_b, parent_a))
    return np.array(offsprings)


offsprings = apply_crossovers(best_individuals)
print(f"\nOffsprings: \n{offsprings}")

def apply_mutations(generation):
    gen_wt_mutations = []
    for path in generation:
        if np.random.randint(0, 1000) < 9:
            index1, index2 = np.random.randint(1, len(path) - 1), np.random.randint(1, len(path) - 1)
            path[index1], path[index2] = path[index2], path[index1]
        gen_wt_mutations.append(path)
    return gen_wt_mutations


def generate_new_population(points, old_generation):
    survivors = selection(old_generation, points)
    crossovers = apply_crossovers(survivors)
    new_population = apply_mutations(crossovers)
    return np.array(new_population)


new_population = generate_new_population(distances_matrix, random_population)
print(f"\nNew population: \n{new_population}")

# Main loop
population = initialize_population()
for i in range(generations):
    population = generate_new_population(distances_matrix, population)
    best_individual = selection(population, distances_matrix)[0]
    _ = system('cls')
    print(f"\nGeneration {i + 1} \nBest individual: {best_individual} \nTotal distance: {total_distance(best_individual, distances_matrix)}")
    #time.sleep(0.01)






