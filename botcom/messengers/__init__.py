import importlib
from abc import ABC, abstractmethod
from typing import Union
from dtos import Message


class Messenger(ABC):
    @staticmethod
    @abstractmethod
    def is_cmd(msg: Message):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def send(id_to: Union[str, int], msg: Message):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def parse(data) -> Message:
        raise NotImplementedError

    @staticmethod
    def get_instance(name: str):
        try:
            module = importlib.import_module(f'{__name__}.{name}')
            return getattr(module, name.capitalize())
        except (ImportError, AttributeError):
            return None
