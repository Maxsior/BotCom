from commands.base import Command
from messengers import Messenger
from storage import Storage
from entities import Message
import l10n


class ChatCommand(Command):
    def execute(self):
        sender = self.msg.sender
        messenger_from = Messenger.get_instance(sender.messenger)

        if len(self.msg.cmd.args) < 2:
            messenger_from.send(sender.id, Message(l10n.format(sender.lang, 'WRONG_ARGS')))
            return

        messenger, id_ = self.msg.cmd.args

        receiver = Storage().find_user(messenger, id_)

        if receiver is None:
            messenger_from.send(sender.id, Message(
                l10n.format(sender.lang, 'INVALID_USER')
            ))
            return

        Storage().update(sender.key, {'receiver': receiver.key})
        messenger_to = Messenger.get_instance(receiver.messenger)

        if receiver.receiver == sender.key:
            message_to_sender = Message(l10n.format(
                sender.lang,
                'CONNECTED',
                name=receiver.name
            ))
            message_to_receiver = Message(l10n.format(
                receiver.lang,
                'CONNECTED',
                name=sender.name
            ))
        else:
            message_to_sender = Message(l10n.format(
                sender.lang,
                'CONN_WAIT',
                name=receiver.name,
                messenger=receiver.messenger
            ))
            message_to_receiver = Message(l10n.format(
                receiver.lang,
                'CONN_NOTIFICATION',
                name=sender.name,
                messenger=sender.messenger,
                id=sender.nick or sender.phone or sender.id
            ))

        messenger_from.send(sender.id, message_to_sender)
        messenger_to.send(receiver.id, message_to_receiver)
