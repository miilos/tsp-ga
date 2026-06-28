from abc import ABC, abstractmethod

from ga.generation_info import GenerationInfo
from observer.subscriber_interface import SubscriberInterface


class PublisherInterface(ABC):
    """ Used to decouple the GA from UI/file writing logic using observer pattern """

    @abstractmethod
    def subscribe(self, subscriber: SubscriberInterface) -> None:
        pass

    @abstractmethod
    def publish(self, message: GenerationInfo) -> None:
        pass
