import random
from cities_provider import CitiesProvider

class Ga:
    POPULATION_SIZE = 10
    MAX_ITERATIONS = 100

    TOURNAMENT_SIZE = 3

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

    # tournament selection - works better than roulette wheel selection because
    # all the tour lengths are too similar, so the odds of selecting the best vs. the worst
    # individual aren't big enough
    def selection(self, population: list[list[int]]) -> list[list[int]]:
        new_population = []

        for _ in range(self.POPULATION_SIZE):
            tournament = random.sample(population, self.TOURNAMENT_SIZE)
            winner = max(tournament, key=lambda individual: self.fitness(individual))
            new_population.append(winner)

        return new_population

    # edge recombination crossover - build an adjacency list and only construct a child path
    # from neighbors of its parents - results in the shortest edges
    def crossover(self, parent1: list[int], parent2: list[int]) -> list[int]:
        adjacency_list = {
            city_id: self._neighbors(city_id, parent1) | self._neighbors(city_id, parent2)
            for city_id in parent1
        }

        child = [random.choice(parent1)]
        while len(child) < len(parent1):
            curr_city_id = child[-1]
            neighbors = adjacency_list[curr_city_id]

            adjacency_list.pop(curr_city_id)
            for neighbors_set in adjacency_list.values():
                neighbors_set.discard(curr_city_id)

            if neighbors:
                min_neighbors = min([len(adjacency_list[city_id]) for city_id in neighbors])
                next_candidates = [city_id for city_id in neighbors if len(adjacency_list[city_id]) == min_neighbors]
                next_city = random.choice(next_candidates)
            else:
                next_city = random.choice([city_id for city_id in adjacency_list])

            child.append(next_city)

        return child

    def _neighbors(self, city_id: int, individual: list[int]) -> set[int]:
        city_idx = individual.index(city_id)
        return { individual[city_idx-1], individual[(city_idx+1) % len(individual)] }

    # reverse mutation - pick two random points and reverse cities between them
    def mutate(self, individual: list[int]) -> list[int]:
        individual = individual.copy()
        start, end = sorted(random.sample(range(len(individual)), 2))
        individual[start:end+1] = list(reversed(individual[start:end+1]))
        return individual
