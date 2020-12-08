import importlib
from abc import ABC, abstractmethod
from typing import Optional, Generator
from entities import Message
from entities.keyboards import Keyboard
import os
import os.path


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

    @staticmethod
    def get_available_messengers() -> Generator[str, None, None]:
        base = os.path.dirname(__file__)
        for item in os.scandir(base):
            if item.is_dir():
                yield item.name
