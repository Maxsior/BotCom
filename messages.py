import logging
import storage


def execute_cmd(msg_data):
    msg = msg_data["message"]
    if msg.startswith(('/reg', '/start', '/рег', '/регистрация')):
        # TODO обработка команды reg / start / рег
        # storage.add_user()
        pass
    elif msg.startswith(('/conn', '/chat', '/подкл', '/чат')):
        pass
        # TODO обработка команды conn / chat / подкл
    elif msg.startswith(('/unreg', '/del', '/delete')):
        pass
        # TODO обработка команды unreg / del / delete
    elif msg.startswith(('/close', '/end', '/off')):
        pass
        # TODO обработка команды close / end / off
    elif msg.startswith(('/help', '/помощь')):
        pass
        # TODO обработка команды help / помощь
    elif msg.startswith('/status'):
        pass
        # TODO обработка команды status
    elif msg.startswith('/change'):
        pass
        # TODO обработка команды change


def normalize(text):
    return text


def parse(msg_data):
    logging.log(msg_data['message'])
    if msg_data["message"].startsWith('/'):
        execute_cmd(msg_data)
    else:
        # TODO обработка сообщения
        msg_data['read_id']
        pass
