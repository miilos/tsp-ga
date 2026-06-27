from cities_provider import CitiesProvider
from ga import Ga

cities_provider = CitiesProvider()
ga = Ga(cities_provider)

population = ga.create_initial_population()

print("====== starting population =======")
for individual in population:
    print("individual: ", individual)
    print("cost: ", ga.calculate_cost(individual))
    print("fitness: ", ga.fitness(individual))

result = ga.run()
print("====== result population =======")
print("individual: ", result)
print("cost: ", ga.calculate_cost(result))