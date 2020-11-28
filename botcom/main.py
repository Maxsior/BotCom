import logging
from flask import Flask, request, abort
from messengers import Messenger
from storage import Storage
import commands
from dtos import User
# import l10n

app = Flask(__name__,
            static_url_path='/',
            static_folder='../pages')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route('/<string:messenger>', methods=['POST'])
def main(messenger):
    messenger_from = Messenger.get_instance(messenger)

    if messenger_from is None:
        abort(404)
        return

    msg = messenger_from.parse(request.json)
    if msg is None:
        return 'ok'

    if Storage.find_user(msg.sender.messenger, msg.sender.id) is None:
        Storage.add_user(msg.sender)
        messenger_from.send(msg.sender.id, None)
        return 'ok'

    if msg.cmd is not None:
        cmd_class = commands.get_class(msg.cmd.name)
        cmd_class(msg).execute()
        return 'ok'

    receiver: User = Storage.get_receiver_id(msg.sender.id)

    if receiver is None:
        messenger_from.send(msg.sender.id, None)
    else:
        messenger_to = Messenger.get_instance(receiver.messenger)
        messenger_to.send(receiver.id, msg)

    return 'ok'


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    app.run(debug=True)
