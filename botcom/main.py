import logging
from flask import Flask, request, abort
from typing import Optional
from entities import Message
import entities.keyboards as keyboards
from messengers import Messenger
from storage import Storage
import commands

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)-15s] %(levelname)s %(filename)s:%(lineno)d | %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/<string:messenger>', methods=['POST'])
def main(messenger):
    messenger_from = Messenger.get_instance(messenger)

    if messenger_from is None:
        abort(404)
        return

    logger.info('Parsing the message')

    msg: Optional[Message] = messenger_from.parse(request.json)

    if msg is None:
        logger.info('Not new message')
        return 'ok'

    logger.info('Message was parsed successfully')

    if not msg.sender.registered:
        logger.info('Registering user')
        msg.sender.key = Storage().add_user(msg.sender)
        logger.info('Sending welcome message')
        messenger_from.send(
            msg.sender.id,
            Message('MESSAGE.REGISTER').localize(msg.sender.lang),
            keyboards.ConnectKeyboard(msg.sender)
        )

        if msg.cmd is None:
            return 'ok'

    if msg.cmd is not None:
        logger.info('Command detected')
        cmd_class = commands.get_class(msg.cmd.name)
        logger.info('Executing command')
        cmd_class(msg).execute()
        return 'ok'

    if msg.sender.receiver is None:
        logger.info('No receiver')
        messenger_from.send(
            msg.sender.id,
            Message('MESSAGE.NO_RECIPIENT').localize(msg.sender.lang),
            keyboards.ConnectKeyboard(msg.sender)
        )
        return 'ok'

    logger.info('Getting receiver')
    receiver = Storage().get_user(msg.sender.receiver)
    if receiver.receiver != msg.sender.key:
        logger.info('Receiver does not confirm the connection')
        messenger_from.send(
            msg.sender.id,
            Message('CONN_WAIT').localize(msg.sender.lang,
                                          name=receiver.name,
                                          messenger=receiver.messenger),
            keyboards.ConnectKeyboard(msg.sender)
        )
        return 'ok'

    logger.info('Getting receiver messenger instance')
    messenger_to = Messenger.get_instance(receiver.messenger)
    logger.info('Forwarding')
    messenger_to.send(
        receiver.id,
        Message('MESSAGE.TEMPLATE', msg.attachments).localize('', name=msg.sender.name, msg=msg.text),
        keyboards.ConnectKeyboard(receiver)
    )

    return 'ok'


if __name__ == '__main__':
    app.run()
