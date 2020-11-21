import storage
import messengers
import strings


def _is_reg_cmd(msg):
    return msg.startswith(('/reg', '/start', '/рег', '/регистрация'))


def _cmd_registration(**kwargs):
    exists = storage.user_exists(kwargs['real_id'], kwargs['messengers'])
    if not exists:
        id_ = storage.add_user(kwargs['real_id'], kwargs['messengers'],
                               kwargs['name'], kwargs['nick'])
    else:
        id_ = storage.get_id(kwargs['real_id'], kwargs['messengers'])
    return id_, exists


def _cmd_connect(id_from, id_to):
    storage.set_current(id_from, id_to)
    name_from = storage.get_name(id_from)
    name_to = storage.get_name(id_to)
    social_from = storage.get_social(id_from)
    social_to = storage.get_social(id_to)

    if storage.get_cur_con(id_to) == id_from:
        send(id_from, strings.CONNECTED.format(name=name_to))
        send(id_to, strings.CONNECTED.format(name=name_from))
    else:
        send(id_from, strings.CONN_WAIT.format(name=name_to,
                                               messenger=social_to))
        send(id_to, strings.CONN_NOTIFICATION.format(name=name_from,
                                                     id=id_from,
                                                     messenger=social_from))

    msgs = storage.get_msgs(id_to, id_from)
    if len(msgs) > 0:
        for msg in msgs:
            msg = strings.MSG.format(name=name_to, msg=msg)
            send(id_from, msg)


def execute_cmd(msg_data):
    msg = msg_data["msg"]
    id_from = storage.get_id(msg_data['real_id'], msg_data['messengers'])

    if _is_reg_cmd(msg):
        id_from, existed = _cmd_registration(**msg_data)

        if not existed:
            send(id_from, strings.HELP)
            send(id_from, '---', keyboard='main')

        send(id_from, strings.REGISTER)

    elif msg.startswith(('/conn', '/chat', '/подкл', '/подключиться', '/чат')):
        args = msg.split()
        size = len(args)
        if size == 1:
            storage.wait(id_from, True)
            send(id_from, strings.WAIT_FOR_PARAMS)
        else:
            storage.wait(id_from, False)

            real_id_to = args[1].upper()
            messenger = args[2].lower()

            if messenger in messengers.modules:
                id_to = storage.get_id(real_id_to, messenger) or \
                         storage.get_id(real_id_to, messenger, by_nick=True)

                if id_to is None:
                    send(id_from, strings.INVALID_USER)
                else:
                    _cmd_connect(id_from, id_to)
            else:
                send(id_from, strings.NO_SOCIAL)

    elif msg.startswith(('/unreg', '/del', '/delete', '/удалить_аккаунт')):
        send(id_from, strings.BYE.format(messenger=msg_data['messengers']),
             keyboard='reset')
        storage.delete_user(id_from)

    elif msg.startswith(('/close', '/off', '/отключиться')):
        id_to = storage.get_cur_con(id_from)
        if id_to is not None:
            storage.set_current(id_from, None)
            send(id_to, strings.FRIEND_OFF)
            send(id_from, strings.OFF)
        else:
            send(id_from, strings.OFF_BLANK)

    elif msg.startswith(('/help', '/помощь')):
        for part in strings.FULL_HELP.split('<--->'):
            send(id_from, part)

    elif msg.startswith(('/status', '/статус')):
        conn_id = storage.get_cur_con(id_from)
        name = storage.get_name(conn_id) if conn_id is not None else ''

        others = storage.get_others(id_from)
        if len(others) == 0:
            others_s = '(Отсутствуют)'
        else:
            others_s = ', '.join(map(
                lambda u: f"{u[0]} ({u[1]} {u[2]})", others)
            )

        send(id_from, strings.STATUS.format(name=name, current=conn_id,
                                            others=others_s))

    else:
        send(id_from, strings.UNDEFINED_CMD)


def send(id_to, msg, **kwargs):
    real_id, social_name = storage.get_real_id(id_to)
    module = messengers.modules[social_name]
    module.send_message(real_id, msg, **kwargs)


def forward(msg_data):
    if not storage.user_exists(msg_data['real_id'], msg_data['messengers']):
        if not _is_reg_cmd(msg_data['msg']):
            msg_data['msg'] = '/reg'
        execute_cmd(msg_data)
        return

    else:
        id_from = storage.get_id(msg_data['real_id'], msg_data['messengers'])
        if storage.is_waiting(id_from):
            msg_data['msg'] = '/conn ' + msg_data['msg']

    if msg_data['msg'].startswith('/'):
        execute_cmd(msg_data)
    else:
        id_to = storage.get_cur_con(id_from)

        if id_to is None:
            send(id_from, strings.NO_RECIPIENT)
            return

        if id_from != storage.get_cur_con(id_to):
            storage.add_msg(id_from, id_to, msg_data['msg'])
        else:
            name = msg_data.get('name') or storage.get_name(id_from)
            msg = strings.MSG.format(
                name=name,
                msg=msg_data['msg']
            )
            send(id_to, msg)
