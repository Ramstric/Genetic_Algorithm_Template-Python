# Traveler's problem - Evolutive algorithm approach
import os
import numpy as np


# Load file
def load_file(file_name):
    file = open(file_name, "r")
    data = file.readlines()
    file.close()
    return data


data = load_file("./Evol/Datos2.txt")

# Data has the following structure:
# First line is the number n of cities
# Read n lines with the name of the cities
# Next n lines are the distances between the cities
# Next line are the cities to visit in the order they should be visited (m lines to read)
# Read m lines with the name of the cities to visit in the order they should be visited
# Next line is the number of individuals in the population
# Next line is the number of generations

# Read number of cities
n = int(data[0])

# Read cities
cities = []
for i in range(1, n + 1):
    cities.append(data[i].strip())

# Read distances
distances = []
for i in range(n + 1, n + 1 + n):
    distances.append(list(map(int, data[i].strip().split())))

distances = np.array(distances)

print(f"Number of cities: {n} \nCities: {cities} \nDistances: {distances}")

# Read cities to visit
m = int(data[n + 1 + n])
cities_to_visit = []

for i in range(n + 2 + n, n + 2 + n + m):
    cities_to_visit.append(data[i].strip())

print(f"\nCities to visit: {cities_to_visit}")

population_size = int(data[n + 2 + n + m])  # Read number of individuals in the population
generations = int(data[n + 3 + n + m])      # Read number of generations
inversion_rate = float(data[n + 4 + n + m])   # Inversion rate
mutation_rate = float(data[n + 5 + n + m])    # Mutation rate

print(f"\nPopulation size: {population_size} \nGenerations: {generations} \nInversion rate: {inversion_rate} \nMutation rate: {mutation_rate}")

# Evolutive algorithm that runs constantly until the user stops it
# It will generate a population of individuals and evolve them through generations
# Must try to minimize the total distance traveled
# The algorithm will print the current total distance of the best individual in the population
# and the current generation

# Generate a random population of individuals
def generate_population(population_size, n):
    population = []
    for i in range(population_size):
        individual = np.random.permutation(n)
        population.append(individual)
    return population

# Calculate the total distance of an individual
def total_distance(individual, distances):
    total = 0
    for i in range(len(individual) - 1):
        total += distances[individual[i]][individual[i + 1]]
    total += distances[individual[-1]][individual[0]]
    return total

# Select the best individuals in the population
def selection(population, distances):
    best_individuals = []
    for individual in population:
        best_individuals.append((individual, total_distance(individual, distances)))
    best_individuals = sorted(best_individuals, key=lambda x: x[1])
    return best_individuals[:int(len(best_individuals) / 2)]

# Crossover two individuals
def crossover(individual1, individual2):
    start = np.random.randint(len(individual1))
    end = np.random.randint(start, len(individual1))
    child = [-1] * len(individual1)
    child[start:end] = individual1[start:end]
    for i in range(len(individual2)):
        if individual2[i] not in child:
            for j in range(len(child)):
                if child[j] == -1:
                    child[j] = individual2[i]
                    break
    return child

# Mutate an individual
def mutate(individual, mutation_rate):
    if np.random.rand() < mutation_rate:
        start = np.random.randint(len(individual))
        end = np.random.randint(start, len(individual))
        individual[start:end] = individual[start:end][::-1]
    return individual

# Evolve the population
def evolve(population, distances, inversion_rate, mutation_rate):
    best_individuals = selection(population, distances)
    new_population = []
    for i in range(len(best_individuals)):
        new_population.append(best_individuals[i][0])
    while len(new_population) < len(population):
        individual1 = best_individuals[np.random.randint(len(best_individuals))][0]
        individual2 = best_individuals[np.random.randint(len(best_individuals))][0]
        child = crossover(individual1, individual2)
        child = mutate(child, mutation_rate)
        new_population.append(child)
    return new_population

# Main loop
population = generate_population(population_size, n)
for i in range(1000):
    population = evolve(population, distances, inversion_rate, mutation_rate)
    best_individual = selection(population, distances)[0]
    print(f"Generation {i + 1} - Best individual: {best_individual[0]} - Total distance: {best_individual[1]}")

os.system("pause")
