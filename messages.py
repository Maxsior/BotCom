import logging
import storage
from social import vk, telegram
import strings


def _cmd_connect(id_from, uid_to):
    id_to = storage.get_id(uid_to)
    if id_to is not None:
        storage.set_current(id_from, id_to)
        uid_from = storage.get_uid(id_from)
        name_from = storage.get_name(id_from)
        name_to = storage.get_name(id_to)

        msgs = storage.get_msgs(id_to, id_from)
        if len(msgs) > 0:
            for msg in msgs:
                msg = strings.MSG.format(name=name_from, msg=msg)
                send(id_from, msg)

        if storage.get_cur_con(id_to) == id_from:
            send(id_from, strings.CONNECTED.format(uid=uid_to, name=name_to))
            send(id_to, strings.CONNECTED.format(uid=uid_from, name=name_from))
        else:
            send(id_from, strings.CONN_WAIT.format(uid=uid_to))
            send(id_to, strings.CONN_NOTIFICATION.format(uid=uid_from,
                                                         name=name_from))
    else:
        send(id_from, strings.INVALID_UID)


def execute_cmd(msg_data):
    msg = msg_data["msg"]
    id_from = storage.get_id(msg_data['real_id'], msg_data['social'])

    if msg.startswith(('/reg', '/start', '/рег', '/регистрация')):
        uid = storage.update_uid(msg_data['real_id'], msg_data['social'])
        send(id_from, strings.NEW_UID.format(uid=uid))

    elif msg.startswith(('/conn', '/chat', '/подкл', '/чат')):
        #TODO подключение по внутреннему идентификатору соц.сети
        # /conn 1234567890 vk
        uid_to = msg.split()[1].upper()  # получаем аргумент команды
        _cmd_connect(id_from, uid_to)

    elif msg.startswith(('/unreg', '/del', '/delete', '/выйти')):
        # TODO уведомление об удалении
        storage.delete_user(id_from)

    elif msg.startswith(('/close', '/end', '/off', '/откл')):
        #TODO уведомление об отключении
        storage.set_current(id_from, None)

    elif msg.startswith(('/help', '/помощь')):
        send(id_from, strings.FULL_HELP)

    elif msg.startswith(('/status', '/статус')):
        others = storage.get_others(id_from)
        conn_id = storage.get_cur_con(id_from)
        if conn_id is not None:
            conn_uid = storage.get_uid(conn_id)
            name = storage.get_name(conn_id)
        else:
            conn_uid = 'Нет собеседника'
            name = ''
        if len(others) == 0:
            others_s = '(Отсутствуют)'
        else:
            others_s = ', '.join(map(lambda user: f"{user[0]} ({user[1]})",
                                 others))
        uid_from = storage.get_uid(id_from)
        send(id_from, strings.STATUS.format(
            uid=uid_from,
            current=conn_uid,
            others=others_s,
            name=name
        ))


def send(id_to, msg):
    real_id, social = storage.get_real_id(id_to)
    if social == vk.NAME:
        vk.send_message(real_id, msg)
    elif social == telegram.NAME:
        telegram.send_message(real_id, msg)


def forward(msg_data):
    logging.debug(msg_data['msg'])

    # if not utils.check_id(msg_data['real_id']):
    #     raise ValueError('Недопустимый id - ' + msg_data['real_id'])

    if not storage.user_exists(msg_data['real_id'], msg_data['social']):
        id_from = storage.add_user(msg_data['real_id'],
                                   msg_data['social'],
                                   msg_data.get('name'))
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
                name = msg_data.get('name') or storage.get_name(id_from)
                msg = strings.MSG.format(
                    name=name,
                    msg=msg_data['msg']
                )
                send(id_to, msg)
