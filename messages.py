import logging
import storage
from social import vk, telegram
import utils
import strings


def execute_cmd(msg_data):
    # TODO обработка команд
    msg = msg_data["msg"]
    id_from = storage.get_id(msg_data['real_id'], msg_data['social'])
    if msg.startswith(('/reg', '/start', '/рег', '/регистрация')):
        uid = storage.update_uid(msg_data['real_id'], msg_data['social'])
        send(id_from, strings.NEW_UID.format(uid=uid))
    elif msg.startswith(('/conn', '/chat', '/подкл', '/чат')):
        uid = msg.split()[1].upper()  # получаем аргумент команды
        id_to = storage.get_id(uid)
        if id_to is not None:
            storage.set_current(id_from, id_to)
            send(id_from, strings.CONNECTED.format(uid=uid))
        else:
            send(id_from, strings.INVALID_UID)
    elif msg.startswith(('/unreg', '/del', '/delete')):
        storage.delete_user(id_from)
    elif msg.startswith(('/close', '/end', '/off')):
        storage.set_current(id_from, None)
    elif msg.startswith(('/help', '/помощь')):
        send(id_from, strings.HELP)
    elif msg.startswith('/status'):
        send(id_from, strings.STATUS.format(
            uid=storage.get_uid(id_from),
            current=storage.get_cur_con(id_from)
        ))


def send(id_to, msg):
    real_id, social = storage.get_real_id(id_to)
    if social == vk.NAME:
        vk.send_message(real_id, msg)
    elif social == telegram.NAME:
        telegram.send_message(real_id, msg)


def forward(msg_data):
    logging.debug(msg_data['msg'])

    # TODO warn: Не во всех соц. сетях идентификатор -- число
    if not utils.check_id(msg_data['real_id']):
        raise ValueError('Недопустимый id - ' + msg_data['real_id'])

    if not storage.user_exists(msg_data['real_id'], msg_data['social']):
        id_from = storage.add_user(msg_data['real_id'], msg_data['social'])
        uid = storage.get_uid(id_from)
        send(id_from, strings.HELP)
        send(id_from, strings.NEW_UID.format(uid=uid))

        if msg_data["msg"].startswith('/reg'):
            return
    else:
        id_from = storage.get_id(msg_data['real_id'], msg_data['social'])

    if msg_data["msg"].startswith('/'):
        execute_cmd(msg_data)
    else:
        id_to = storage.get_cur_con(id_from)
        if id_to is None:
            send(id_from, strings.NO_RECIPIENT)
        else:
            if id_from != storage.get_cur_con(id_to):
                storage.add_msg(id_from, id_to, msg_data['msg'])
            else:
                send(id_to, msg_data['msg'])
