from dtos import Message, CommandInfo
from commands.chat import ChatCommand


class ChatCommandAlias(ChatCommand):
    def __init__(self, msg: Message):
        super().__init__(Message(
            sender=msg.sender,
            cmd=CommandInfo('chat', [msg.cmd.name, *msg.cmd.args])
        ))
