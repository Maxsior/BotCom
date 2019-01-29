def execute(msg):
    """

    :type msg: str
    """
    if msg.startswith(('/reg', '/start', '/рег', '/регистрация')):
        pass
        # TODO обработка команды reg / start / рег
    elif msg.startswith(('/conn', '/chat', '/подкл', '/чат')):
        pass
        # TODO обработка команды conn / chat / подкл
    elif msg.startswith(('/unreg', '/del', '/delete', 'убейсяобстену')):
        pass
        # TODO обработка команды unreg / del / delete
    elif msg.startswith(('/close', '/end', '/off')):
        pass
        # TODO обработка команды close / end / off
    elif msg.startswith(('/help', '/помощь')):
        pass
        # TODO обработка команды help / помощь
