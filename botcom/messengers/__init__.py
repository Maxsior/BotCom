import importlib.util
from abc import ABC, abstractmethod
from typing import Optional, List
from entities import Message
import entities.keyboards as keyboards
import os
import os.path


class Messenger(ABC):
    @staticmethod
    @abstractmethod
    def create_keyboard(keyboard: 'keyboards.Keyboard'):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def send(id_to: str, msg: Message, keyboard: Optional['keyboards.Keyboard']):
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
        spec = importlib.util.find_spec(f'{__name__}.{name}')
        if spec:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return getattr(module, name.capitalize())
        else:
            return None


def get_available_messengers() -> List[str]:
    base = os.path.dirname(__file__)
    return [item.name
            for item in os.scandir(base)
            if item.is_dir() and not item.name.startswith(('__', '.'))]
