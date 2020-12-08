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
            messenger_from.send(sender.id, Message('MESSAGE.WRONG_ARGS').localize(sender.lang))
            return

        messenger, id_ = self.msg.cmd.args

        receiver = Storage().find_user(messenger, id_)

        if receiver is None:
            messenger_from.send(sender.id, Message('MESSAGE.INVALID_USER').localize(sender.lang))
            return

        Storage().update(sender.key, {'receiver': receiver.key})
        messenger_to = Messenger.get_instance(receiver.messenger)

        if receiver.receiver == sender.key:
            message_to_sender = Message('MESSAGE.CONNECTED').localize(sender.lang, name=receiver.name)
            message_to_receiver = Message('MESSAGE.CONNECTED').localize(receiver.lang, name=sender.name)
        else:
            message_to_sender = Message('MESSAGE.CONN_WAIT').localize(sender.lang, name=receiver.name)
            message_to_receiver = Message('MESSAGE.CONN_NOTIFICATION')\
                .localize(receiver.lang,
                          name=sender.name,
                          messenger=sender.messenger,
                          id=sender.nick or sender.phone or sender.id
                          )

        messenger_from.send(sender.id, message_to_sender)
        messenger_to.send(receiver.id, message_to_receiver)
