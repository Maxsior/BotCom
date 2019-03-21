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
                msg = strings.MSG.format(name=name_to, msg=msg)
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

    elif msg.startswith(('/conn', '/chat', '/подкл', '/подключиться', '/чат')):
        args = msg.split()
        size = len(args)
        if size == 1:
            storage.wait(id_from, True)
            send(id_from, strings.WAIT_FOR_PARAMS)
        elif size == 2:
            storage.wait(id_from, False)
            uid_to = args[1].upper()  # получаем аргумент команды
            _cmd_connect(id_from, uid_to)
        else:
            storage.wait(id_from, False)

            real_id_to = args[1].upper()
            social = args[2].lower()

            if social in (vk.NAME, telegram.NAME):
                uid_to = storage.get_uid(
                    storage.get_id(real_id_to, social) or
                    storage.get_id(real_id_to, social, by_nick=True)
                )

                if uid_to is None:
                    send(id_from, strings.INVALID_USER)
                else:
                    _cmd_connect(id_from, uid_to)
            else:
                send(id_from, strings.NO_SOCIAL)

    elif msg.startswith(('/unreg', '/del', '/delete', '/удалить_аккаунт')):
        send(id_from,
             strings.BYE.format(social=msg_data['social']),
             keyboard='reset')
        storage.delete_user(id_from)

    elif msg.startswith(('/close', '/off', '/отключиться')):
        storage.set_current(id_from, None)
        send(id_from, strings.OFF)

    elif msg.startswith(('/help', '/помощь')):
        for part in strings.FULL_HELP.split('<--->'):
            send(id_from, part)

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
            others_s = ', '.join(map(lambda u: f"{u[0]} ({u[1]})", others))
        uid_from = storage.get_uid(id_from)
        send(id_from, strings.STATUS.format(
            uid=uid_from,
            current=conn_uid,
            others=others_s,
            name=name
        ))
    else:
        send(id_from, strings.UNDEFINED_CMD)


def send(id_to, msg, **kwargs):
    real_id, social = storage.get_real_id(id_to)
    if social == vk.NAME:
        vk.send_message(real_id, msg, **kwargs)
    elif social == telegram.NAME:
        telegram.send_message(real_id, msg, **kwargs)


def forward(msg_data):
    logging.debug(msg_data['msg'])

    if not storage.user_exists(msg_data['real_id'], msg_data['social']):
        id_from = storage.add_user(msg_data['real_id'], msg_data['social'],
                                   msg_data['name'], msg_data['nick'])
        uid = storage.get_uid(id_from)
        send(id_from, strings.HELP)
        send(id_from, strings.NEW_UID.format(uid=uid), keyboard='main')

        if msg_data["msg"].startswith(('/reg', '/start', '/рег',
                                       '/регистрация')):
            return
    else:
        id_from = storage.get_id(msg_data['real_id'], msg_data['social'])

        if storage.is_waiting(id_from):
            msg_data['msg'] = '/conn ' + msg_data['msg']

    if msg_data['msg'].startswith('/'):
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
