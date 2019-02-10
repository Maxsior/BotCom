import logging
import storage
from social import vk, telegram
import strings


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


def normalize(text):
    # TODO нужна ли нормализация?
    return text


def send(id_to, msg):
    real_id, social = storage.get_real_id(id_to)
    if social == 'vk':
        vk.send_message(real_id, msg)
    elif social == 'telegram':
        telegram.send_message(real_id, msg)


def forward(msg_data):
    logging.debug(msg_data['msg'])
    if msg_data["msg"].startswith('/'):
        execute_cmd(msg_data)
    else:
        id_from = storage.get_id(msg_data['real_id'], msg_data['social'])
        id_to = storage.get_cur_con(id_from)
        if id_to is None:
            send(id_from, strings.NO_RECIPIENT)
        else:
            if id_from != storage.get_cur_con(id_to):
                storage.add_msg(id_from, id_to, msg_data['msg'])
            else:
                send(id_to, msg_data['msg'])
