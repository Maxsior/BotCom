import logging
import storage
from social import vk, telegram

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
    # TODO нужна ли нормализация?
    return text


def parse(msg_data):
    logging.debug(msg_data['message'])
    if msg_data["message"].startsWith('/'):
        execute_cmd(msg_data)
    else:
        id_from = storage.get_id(msg_data['read_id'], msg_data['social'])
        id_to = storage.get_cur_con(id_from)
        if id_from != storage.get_cur_con(id_to):
            storage.add_msg(id_from, id_to, msg_data['msg'])
        else:
            if msg_data['social'] == 'vk':
                vk.send_message(
                        storage.get_uid(msg_data['read_id'],
                                        msg_data['social'])
                )
            elif msg_data['social'] == 'telegram':
                telegram.send_message(
                        storage.get_uid(msg_data['read_id'],
                                        msg_data['social'])
                )
