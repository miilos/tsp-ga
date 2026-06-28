from abc import ABC, abstractmethod

from ga.generation_info import GenerationInfo


class SubscriberInterface(ABC):
    """ Used to decouple the GA from UI/file writing logic using observer pattern """

    @abstractmethod
    def update(self, generation_info: GenerationInfo) -> None:
        pass