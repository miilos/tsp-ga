from cities_provider import CitiesProvider
from ga import Ga

cities_provider = CitiesProvider()
ga = Ga(cities_provider)

population = ga.create_initial_population()

print(population[0])
print(population[1])
ga.crossover(population[0], population[1])

# for individual in population:
#     print("individual: ", individual)
#     print("cost: ", ga.calculate_cost(individual))
#     print("fitness: ", ga.fitness(individual))
#
# print("------------ new population ---------------")
#
# new_population = ga.selection(population)
# for individual in new_population:
#     print("individual: ", individual)
#     print("cost: ", ga.calculate_cost(individual))
#     print("fitness: ", ga.fitness(individual))