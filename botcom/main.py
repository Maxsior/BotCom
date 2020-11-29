import logging
from flask import Flask, request, abort
from typing import Optional
from entities import Message
from messengers import Messenger
from storage import Storage
import commands
import l10n

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route('/<string:messenger>', methods=['POST'])
def main(messenger):
    messenger_from = Messenger.get_instance(messenger)

    if messenger_from is None:
        abort(404)
        return

    msg: Optional[Message] = messenger_from.parse(request.json)
    if msg is None:
        return 'ok'

    if msg.sender.is_registered is None:
        Storage().add_user(msg.sender)
        messenger_from.send(msg.sender.id, Message(l10n.format(msg.sender.lang, 'REGISTER')))

        if msg.cmd is None:
            return 'ok'

    if msg.cmd is not None:
        cmd_class = commands.get_class(msg.cmd.name)
        cmd_class(msg).execute()
        return 'ok'

    receiver = Storage().get_user(msg.sender.id)

    if receiver is None:
        messenger_from.send(msg.sender.id, Message(l10n.format(msg.sender.lang, 'NO_RECIPIENT')))
    else:
        messenger_to = Messenger.get_instance(receiver.messenger)
        messenger_to.send(receiver.id, msg)

    return 'ok'


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    app.run(debug=True)
