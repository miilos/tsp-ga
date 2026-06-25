import random
from cities_provider import CitiesProvider

class Ga:
    POPULATION_SIZE = 10
    MAX_ITERATIONS = 100

    def __init__(self, cities_provider: CitiesProvider):
        self.cities_provider = cities_provider

    def create_initial_population(self)-> list[list[int]]:
        cities = self.cities_provider.get_cities()
        ids = [c.id for c in cities]

        initial_population = []
        for _ in range(Ga.POPULATION_SIZE):
            individual = ids[:]
            random.shuffle(individual)
            initial_population.append(individual)

        return initial_population

    def calculate_cost(self, individual: list[int]) -> float:
        distances = []

        for i in range(len(individual)):
            curr_city_idx = individual[i]
            next_city_idx = individual[(i+1) % len(individual)]

            curr_city = self.cities_provider.get_city_by_id(curr_city_idx)
            next_city = self.cities_provider.get_city_by_id(next_city_idx)

            distances.append(curr_city.distance_to(next_city))

        return sum(distances)

    def fitness(self, individual: list[int]) -> float:
        return 1 / self.calculate_cost(individual)
