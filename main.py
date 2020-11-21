import logging
from flask import Flask, request, abort, send_file
import messages
import messengers

app = Flask(__name__,
            static_url_path='/',
            static_folder='pages')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route('/<string:messenger>', methods=['POST'])
def main(messenger):
    logger.info(f'request to "{messenger}"')

    data = request.json

    if messenger in messengers.modules:
        module = messengers.modules[messenger]
        result = module.parse(data)
        messages.forward(result)
        return 'ok'
    else:
        logger.warning(f'unknown target "{messenger}" with {data}')
        logger.warning(str(data))
        abort(404)


@app.route('/', methods=['GET'])
def site():
    return send_file('pages/index.html')


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    app.run(debug=True)
