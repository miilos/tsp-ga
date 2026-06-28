import random
import time
from math import floor
from city.cities_provider import CitiesProvider
from ga.generation_info import GenerationInfo
from observer.publisher_interface import PublisherInterface
from observer.subscriber_interface import SubscriberInterface


class Ga(PublisherInterface):
    POPULATION_SIZE = 50
    MAX_SAME_ITERATIONS = 10
    GENERATION_CAP = 1000

    TOURNAMENT_SIZE = 3
    MUTATION_RATE = 0.2
    ELITISM_RATE = 0.2

    def __init__(self, cities_provider: CitiesProvider, generation_delay: float = 0.0):
        self.cities_provider = cities_provider
        self.subscribers = []
        self.generation_delay = generation_delay

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

    # returns list of individuals from the previous population to keep in the next
    def elitism(self, population: list[list[int]]) -> list[list[int]]:
        elitism_count = max(1, floor(len(population) * self.ELITISM_RATE))
        fitness_list = sorted(population, key=lambda individual: self.fitness(individual), reverse=True)
        return fitness_list[:elitism_count]

    def run(self) -> list[int]:
        population = self.create_initial_population()

        generation = 0
        same_iter_count = 0
        prev_best_cost = float("inf")
        while same_iter_count < self.MAX_SAME_ITERATIONS and generation < self.GENERATION_CAP:
            tournament_winners = self.selection(population)

            new_population = []
            for parent1, parent2 in zip(tournament_winners[::2], tournament_winners[1::2]):
                # edge recombination produces n/2 children, crossover each pair twice to get to n children
                new_population.extend((self.crossover(parent1, parent2), self.crossover(parent2, parent1)))

            for i in range(len(new_population)):
                if random.random() < self.MUTATION_RATE:
                    new_population[i] = self.mutate(new_population[i])

            elitism_individuals = self.elitism(population)
            new_population[:len(elitism_individuals)] = elitism_individuals

            population = new_population

            curr_best_individual = sorted(population, key=lambda individual: self.fitness(individual), reverse=True)[0]
            curr_best_cost = self.calculate_cost(curr_best_individual)
            curr_best_fitness = self.fitness(curr_best_individual)

            if curr_best_cost < prev_best_cost:
                prev_best_cost = curr_best_cost
                same_iter_count = 0
            else:
                same_iter_count += 1

            message = GenerationInfo(
                population,
                curr_best_individual,
                curr_best_cost,
                curr_best_fitness,
                generation,
            )
            self.publish(message)

            if self.generation_delay:
                time.sleep(self.generation_delay)

            generation += 1

        return max(population, key=lambda individual: self.fitness(individual))

    def subscribe(self, subscriber: SubscriberInterface) -> None:
        self.subscribers.append(subscriber)

    def publish(self, message: GenerationInfo) -> None:
        for subscriber in self.subscribers:
            subscriber.update(message)
