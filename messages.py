import logging
import storage
from social import vk, telegram
import strings


def execute_cmd(msg_data):
    # TODO обработка команд
    msg = msg_data["msg"]
    if msg.startswith(('/reg', '/start', '/рег', '/регистрация')):
        id_ = storage.get_id(msg_data['real_id'], msg_data['social'])
        uid = storage.update_uid(msg_data['real_id'], msg_data['social'])
        send(id_, strings.NEW_UID.format(uid=uid))
    elif msg.startswith(('/conn', '/chat', '/подкл', '/чат')):
        id_from = storage.get_id(msg_data['real_id'], msg_data['social'])
        uid = msg.split()[1].upper()  # получаем аргумент команды
        id_to = storage.get_id(uid)
        storage.set_current(id_from, id_to)
    elif msg.startswith(('/unreg', '/del', '/delete')):
        id_ = storage.get_id(msg_data['real_id'], msg_data['social'])
        storage.delete_user(id_)
    elif msg.startswith(('/close', '/end', '/off')):
        id_ = storage.get_id(msg_data['real_id'], msg_data['social'])
        storage.set_current(id_, None)
    elif msg.startswith(('/help', '/помощь')):
        pass
    elif msg.startswith('/status'):
        pass


def send(id_to, msg):
    real_id, social = storage.get_real_id(id_to)
    if social == vk.NAME:
        vk.send_message(real_id, msg)
    elif social == telegram.NAME:
        telegram.send_message(real_id, msg)


# TODO issue: SQL injection
def forward(msg_data):
    logging.debug(msg_data['msg'])

    if type(msg_data['real_id']) != int:
        raise ValueError('Недопустимый id - ' + msg_data['real_id'])

    if not storage.user_exists(msg_data['real_id'], msg_data['social']):
        id_from = storage.add_user(msg_data['real_id'], msg_data['social'])
        uid = storage.get_uid(id_from)
        send(id_from, strings.NEW_UID.format(uid=uid))
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
