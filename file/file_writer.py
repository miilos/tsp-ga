import os

from ga.generation_info import GenerationInfo
from observer.subscriber_interface import SubscriberInterface


class FileWriter(SubscriberInterface):
    def __init__(self, file_path: str):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        open(file_path, "w").close()

    def update(self, generation_info: GenerationInfo) -> None:
        try:
            with open(self.file_path, "a") as f:
                # generation_str = "\n".join([str(individual) for individual in generation_info.generation])
                f.write(f"""

                    ===== GENERATION {generation_info.generation_num} =====
                    
                    Best individual: {str(generation_info.best_individual)}
                    Distance: {generation_info.best_cost}
                    Fitness: {generation_info.best_fitness}
                    
                """)
        except OSError:
            pass
