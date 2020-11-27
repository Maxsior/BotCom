from abc import ABC, abstractmethod
import importlib


class Command(ABC):
    @abstractmethod
    def execute(self, *args):
        raise NotImplementedError

    @staticmethod
    def get_instance(name: str):
        try:
            module = importlib.import_module(f'{__name__}.{name}')
            return getattr(module, f'{name.capitalize()}Command')
        except (ImportError, AttributeError):
            return None
