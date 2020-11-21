import logging
from flask import Flask, request, abort, send_file
import messengers
from dtos import User

app = Flask(__name__,
            static_url_path='/',
            static_folder='../pages')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route('/<string:messenger>', methods=['POST'])
def main(messenger):
    logger.info(f'request to "{messenger}"')
    data = request.json

    messenger_from = messengers.get_class(messenger)
    msg = messenger_from.parse(data)

    receiver: User = Storage.get_receiver(msg.sender.id)
    messenger_to = messengers.get_class(receiver.messenger)

    if messenger_to is None:
        messenger_from.send(msg.sender.id, MESSENGER_NOT_FOUND)
        return

    # if detect_cmd(msg):
    #     cmd = <build command by msg>
    #     cmd.execute()
    #     return
    # else:

    messenger_to.send(receiver.id, msg)


@app.route('/', methods=['GET'])
def site():
    return send_file('../pages/index.html')


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    app.run(debug=True)
