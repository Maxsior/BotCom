from commands.base import Command
from storage import Storage
from messengers import Messenger
from entities import Message
import l10n


class UnregCommand(Command):
    def execute(self):
        sender = self.msg.sender

        for connected in Storage().get_connected(sender.key):
            Storage().update(connected.key, {'receiver': None})
            messenger_to = Messenger.get_instance(connected.messenger)
            messenger_to.send(connected.id, Message(l10n.format(connected.lang, 'FRIEND_OFF')))

        Storage().delete(sender.key)
        messenger = Messenger.get_instance(sender.messenger)
        messenger.send(sender.id, Message(l10n.format(
            sender.lang, 'BYE',
            messenger=sender.messenger
        )))
