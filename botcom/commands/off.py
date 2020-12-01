from commands.base import Command
from storage import Storage
from messengers import Messenger
from entities import Message
import l10n


class OffCommand(Command):
    def execute(self):
        sender = self.msg.sender
        messenger_from = Messenger.get_instance(sender.messenger)
        if sender.receiver is not None:
            receiver = Storage().get_user(sender.receiver)
            Storage().update(sender.key, {'receiver': None})
            Storage().update(receiver.key, {'receiver': None})
            messenger_to = Messenger.get_instance(receiver.messenger)
            messenger_to.send(sender.id, Message(l10n.format(sender.lang, 'FRIEND_OFF')))
            messenger_from.send(sender.id, Message(l10n.format(sender.lang, 'OFF')))
        else:
            messenger_from.send(sender.id, Message(l10n.format(sender.lang, 'OFF_BLANK')))