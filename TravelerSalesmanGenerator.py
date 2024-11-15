import numpy as np
import os

# This program wil generate a file with the data for the Traveler Salesman problem

# Number of cities
n = 50

# List of cities
cities = [f"C{i}" for i in range(n)]

# Distances between cities
distances = np.random.randint(1, 1000, (n, n))

# Set diagonal to 0
for i in range(n):
    distances[i, i] = 0

# Cities to visit
m = 25

cities_to_visit = np.random.choice(cities, m, replace=False)

# Number of individuals in the population
population_size = 20

# Number of generations
generations = 20

# Inversion rate
inversion_rate = 0.8

# Mutation rate
mutation_rate = 0.2

# Write data to file
file = open("./Evol/DatosCustom.txt", "w")

file.write(f"{n}\n")
for city in cities:
    file.write(f"{city}\n")

for i in range(n):
    file.write(" ".join(map(str, distances[i])) + "\n")

file.write(f"{m}\n")
for city in cities_to_visit:
    file.write(f"{city}\n")

file.write(f"{population_size}\n")

file.write(f"{generations}\n")

file.write(f"{inversion_rate}\n")

file.write(f"{mutation_rate}\n")

file.close()


