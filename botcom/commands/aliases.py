from commands.chat import ChatCommand
from dtos import Message, Command


class ChatCommandAlias(ChatCommand):
    def __init__(self, msg: Message):
        super().__init__(Message(
            sender=msg.sender,
            cmd=Command('chat', [msg.cmd.name, *msg.cmd.args])
        ))
