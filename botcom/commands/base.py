from abc import ABC, abstractmethod
from dtos import Message


class Command(ABC):
    def __init__(self, msg: Message):
        self.msg = msg

    @abstractmethod
    def execute(self):
        raise NotImplementedError
