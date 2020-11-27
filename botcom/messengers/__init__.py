import importlib
from abc import ABC, abstractmethod
from typing import Optional, Union
from dtos import Message


class Messenger(ABC):
    @staticmethod
    @abstractmethod
    def send(id_to: Union[str, int], msg: Message):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def parse(data) -> Message:
        raise NotImplementedError


def get_class(name: str) -> Optional[Messenger]:
    try:
        module = importlib.import_module(f'{__name__}.{name}')
        return getattr(module, name.capitalize())
    except (ImportError, AttributeError):
        return None
