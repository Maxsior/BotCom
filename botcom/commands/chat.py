from commands.base import Command
from messengers import Messenger
from storage import Storage
from dtos import Message
import l10n


class ChatCommand(Command):
    def execute(self):
        messenger, id_ = self.msg.cmd.args
        sender = Storage.find_user(self.msg.sender.messenger, self.msg.sender.id)
        messenger_from = Messenger.get_instance(sender['messenger'])

        receiver = Storage.find_user(messenger, id_)

        if receiver is None:
            messenger_from.send(sender['id'], Message(
                l10n.format(sender['lang'], 'INVALID_USER')
            ))
            return

        Storage.update_receiver(sender['key'], receiver['key'])
        messenger_to = Messenger.get_instance(receiver['messenger'])

        if receiver.get('receiver') == sender['key']:
            message_to_sender = Message(l10n.format(
                sender.get('lang'),
                'CONNECTED',
                name=receiver['name']
            ))
            message_to_receiver = Message(l10n.format(
                receiver.get('lang'),
                'CONNECTED',
                name=sender['name']
            ))
        else:
            message_to_sender = Message(l10n.format(
                sender.get('lang'),
                'CONN_WAIT',
                name=receiver['name'],
                messenger=receiver['messenger']
            ))
            message_to_receiver = Message(l10n.format(
                receiver.get('lang'),
                'CONN_NOTIFICATION',
                name=sender['name'],
                messenger=sender['messenger'],
                id=sender.get('nick') or sender.get('phone') or sender['id']
            ))

        messenger_from.send(sender['id'], message_to_sender)
        messenger_to.send(receiver['id'], message_to_receiver)
