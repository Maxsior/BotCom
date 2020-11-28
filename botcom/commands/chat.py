from commands import Command
from messengers import Messenger
from storage import Storage


class ChatCommand(Command):
    def execute(self):
        messenger, id_ = self.msg.cmd.args
        sender = Storage.find_user(self.msg.sender.messenger, self.msg.sender.id)
        receiver = Storage.find_user(messenger, id_)
        Storage.update_receiver(sender['key'], receiver['key'])

        messenger_from = Messenger.get_instance(sender.messenger)
        messenger_to = Messenger.get_instance(receiver.messenger)

        messenger_from.send(sender.id, None)
        messenger_to.send(receiver.id, None)
