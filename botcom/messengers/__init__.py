import importlib
from abc import ABC, abstractmethod
from typing import Optional
from entities import Message, Keyboard


class Messenger(ABC):
    @staticmethod
    @abstractmethod
    def create_keyboard(keyboard: Keyboard):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def send(id_to: str, msg: Message, keyboard: Optional[Keyboard]):
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
