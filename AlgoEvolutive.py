#import time
from os import system
import numpy as np
from GeneticAlgorithm.AlgoEvolutive_Classes import Population


# Custom fitness functions
def total_distance(individuals, dist, labels_dict):
    for individual in individuals:

        # Start the route from Madrid
        total = dist[labels_dict["Madrid"]][labels_dict[individual.chromosome[0]]]

        for i in range(len(individual.chromosome) - 1):
            total += dist[labels_dict[individual.chromosome[i]]][labels_dict[individual.chromosome[i + 1]]]

        # End back in Madrid
        total += dist[labels_dict[individual.chromosome[-1]]][labels_dict["Madrid"]]

        individual.fitness = total

    return [individual.fitness for individual in individuals]


def read_data(file_name):
    file = open(file_name, "r")
    data = file.readlines()
    file.close()

    n = int(data[0])  # Number of cities
    cities = []
    for i in range(1, n + 1):
        cities.append(data[i].strip())

    # Distances between cities
    _distances = []
    for i in range(n + 1, n + 1 + n):
        _distances.append(list(map(int, data[i].strip().split())))
    _distances = np.array(_distances)

    _city_to_index = {label: i for i, label in enumerate(cities)}  # Dict to translate labels to indexes

    #print(f"Number of points: {n} \nLabels: {cities} \nDistances: \n{_distances}")

    # Cities to visit
    m = int(data[n + 1 + n])
    _cities_to_visit = []
    for i in range(n + 2 + n, n + 2 + n + m):
        _cities_to_visit.append(data[i].strip())

    #print(f"\nPoints to visit: {_cities_to_visit}")

    _population_size = int(data[n + 2 + n + m])      # Read the number of individuals in the population
    _generations = int(data[n + 3 + n + m])          # Read number of generations
    _crossover_rate = float(data[n + 4 + n + m])     # Crossover rate
    _mutation_rate = float(data[n + 5 + n + m])      # Mutation rate
    return _distances, _city_to_index, _cities_to_visit, _population_size, _generations, _crossover_rate, _mutation_rate


distances, city_to_index, cities_to_visit, population_size, generations, crossover_rate, mutation_rate = read_data("./Evol/Datos2.txt")

# Initialize population
poblacion = Population(cities_to_visit, population_size, total_distance, mutation_rate=90, crossover_rate=100)
poblacion.fitness_evaluation(distances, city_to_index)

poblacion.show_population = False

# Continue evolving
#while True:
#    _ = system('cls')
#    print(poblacion)
#    poblacion.evolve(distances, city_to_index)

gen_max = 1000
while gen_max >= 0:
    poblacion.evolve(distances, city_to_index)
    gen_max -= 1

    if gen_max == 0:
        print(poblacion)
        gen_max = 1000

