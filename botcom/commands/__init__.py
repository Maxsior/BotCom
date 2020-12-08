from commands.wrong_cmd import WrongCmdCommand
from commands.chat import ChatCommand
from commands.help import HelpCommand
from commands.off import OffCommand
from commands.unreg import UnregCommand
from commands.lang import LangCommand
from commands.keyboard import KeyboardCommand
from commands.empty import EmptyCommand
from commands.chat_alias import ChatCommandAlias
from messengers import Messenger

commands = {
    **{messenger: ChatCommandAlias for messenger in Messenger.get_available_messengers()},
    'chat': ChatCommand,
    'help': HelpCommand,
    'lang': LangCommand,
    'off': OffCommand,
    'unreg': UnregCommand,
    'keyboard': KeyboardCommand,
    'empty': EmptyCommand,
}


def get_class(name: str):
    return commands.get(name, WrongCmdCommand)
