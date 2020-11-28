from abc import ABC, abstractmethod
from dtos import Message

from commands.wrong_cmd import WrongCmdCommand
from commands.chat import ChatCommand
from commands.help import HelpCommand
from commands.aliases import ChatCommandAlias

commands = {
    # TODO get list of messengers dynamically
    'vk': ChatCommandAlias,
    'viber': ChatCommandAlias,
    'telegram': ChatCommandAlias,
    'discord': ChatCommandAlias,
    # ...
    'chat': ChatCommand,
    'help': HelpCommand,
    # 'off': OffCommand,
    # 'unreg': UnregCommand,
    # 'status': StatusCommand,
    # 'lang': LangCommand,
}


class Command(ABC):
    def __init__(self, msg: Message):
        self.msg = msg

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @staticmethod
    def get_class(name: str):
        return commands.get(name, WrongCmdCommand)
