from commands.base import Command
from messengers import Messenger
from entities import Message
from storage import Storage
import l10n


class LangCommand(Command):
    def execute(self):
        sender = self.msg.sender
        messenger = Messenger.get_instance(sender.messenger)

        if len(self.msg.cmd.args) == 0:
            messenger.send(sender.id, Message('MESSAGE.WRONG_ARGS').localize(sender.lang))
            return

        lang = self.msg.cmd.args[0]
        Storage().update(sender.key, {'lang': lang})
        messenger.send(sender.id, Message('MESSAGE.LANG_CHANGED').localize(lang))
