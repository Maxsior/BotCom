import logging
from flask import Flask, request, abort
from typing import Optional
from entities import Message
from messengers import Messenger
from storage import Storage
import commands
import l10n

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)-15s] %(levelname)s %(filename)s:%(lineno)d | %(message)s')

app = Flask(__name__)


@app.route('/<string:messenger>', methods=['POST'])
def main(messenger):
    messenger_from = Messenger.get_instance(messenger)

    if messenger_from is None:
        abort(404)
        return

    logging.info('Parsing the message')

    msg: Optional[Message] = messenger_from.parse(request.json)

    if msg is None:
        logging.info('Not new message')
        return 'ok'

    logging.info('Message was parsed successfully')

    if not msg.sender.registered:
        logging.info('Registering user')
        msg.sender.key = Storage().add_user(msg.sender)
        logging.info('Sending welcome message')
        messenger_from.send(msg.sender.id, Message('MESSAGE.REGISTER').localize(msg.sender.lang))

        if msg.cmd is None:
            return 'ok'

    if msg.cmd is not None:
        logging.info('Command detected')
        cmd_class = commands.get_class(msg.cmd.name)
        logging.info('Executing command')
        cmd_class(msg).execute()
        return 'ok'

    if msg.sender.receiver is None:
        logging.info('No receiver')
        messenger_from.send(msg.sender.id, Message('MESSAGE.NO_RECIPIENT').localize(msg.sender.lang))
        return 'ok'

    logging.info('Getting receiver')
    receiver = Storage().get_user(msg.sender.receiver)
    if receiver.receiver != msg.sender.key:
        logging.info('Receiver does not confirm the connection')
        messenger_from.send(
            msg.sender.id,
            Message('CONN_WAIT').localize(msg.sender.lang,
                                          name=receiver.name,
                                          messenger=receiver.messenger)
        )
        return 'ok'

    logging.info('Getting receiver messenger instance')
    messenger_to = Messenger.get_instance(receiver.messenger)
    logging.info('Forwarding')
    messenger_to.send(
        receiver.id,
        Message('MESSAGE.TEMPLATE', msg.attachments).localize('', name=msg.sender.name, msg=msg.text)
    )

    return 'ok'


if __name__ == '__main__':
    app.run()
