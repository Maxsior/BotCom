from commands.wrong_cmd import WrongCmdCommand
from commands.chat import ChatCommand
from commands.help import HelpCommand
from commands.off import OffCommand
from commands.unreg import UnregCommand
# from commands.status import StatusCommand
from commands.lang import LangCommand
from commands.chat_alias import ChatCommandAlias

commands = {
    # TODO get list of messengers dynamically
    'vk': ChatCommandAlias,
    'viber': ChatCommandAlias,
    'telegram': ChatCommandAlias,
    'discord': ChatCommandAlias,
    # ...
    'chat': ChatCommand,
    'help': HelpCommand,
    # 'status': StatusCommand,
    'lang': LangCommand,
    'off': OffCommand,
    'unreg': UnregCommand,
}


def get_class(name: str):
    return commands.get(name, WrongCmdCommand)
