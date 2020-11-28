import importlib
from abc import ABC, abstractmethod
from typing import Union, Optional
from dtos import Message, User


class Messenger(ABC):
    @staticmethod
    @abstractmethod
    def send(id_to: User, msg: Message):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def parse(data) -> Optional[Message]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def parse_cmd(msg):
        raise NotImplementedError

    @staticmethod
    def get_instance(name: str):
        try:
            module = importlib.import_module(f'{__name__}.{name}')
            return getattr(module, name.capitalize())
        except (ImportError, AttributeError):
            return None
