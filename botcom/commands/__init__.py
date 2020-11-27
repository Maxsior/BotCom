from abc import ABC, abstractmethod


class Command(ABC):
    @staticmethod
    @abstractmethod
    def execute(*args, **kwargs):
        raise NotImplementedError
