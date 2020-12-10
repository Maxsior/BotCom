from commands.base import Command
from messengers import Messenger
from entities import Message
import entities.keyboards as keyboards


class KeyboardCommand(Command):
    def execute(self):
        sender = self.msg.sender
        messenger = Messenger.get_instance(sender.messenger)

        if len(self.msg.cmd.args) == 0:
            messenger.send(
                sender.id,
                Message('MESSAGE.WRONG_ARGS').localize(sender.lang),
                keyboards.ConnectKeyboard(sender)
            )
            return

        keyboard = self.msg.cmd.args[0]

        try:
            messenger.send(
                sender.id,
                Message(f'KEYBOARD.{keyboard.upper()}').localize(sender.lang),
                getattr(keyboards, f'{keyboard.capitalize()}Keyboard')(sender)
            )
        except KeyError:
            messenger.send(
                sender.id,
                Message('MESSAGE.WRONG_ARGS').localize(sender.lang),
                keyboards.ConnectKeyboard(sender)
            )
