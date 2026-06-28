class GenerationInfo:
    def __init__(
        self,
        generation: list[list[int]],
        best_individual: list[int],
        best_cost: float,
        best_fitness: float,
        generation_num: int
    ):
        self.generation = generation
        self.best_individual = best_individual
        self.best_cost = best_cost
        self.best_fitness = best_fitness
        self.generation_num = generation_num