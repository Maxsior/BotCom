def configure_logger():
    global logger_configured
    if not logger_configured:
        import logging
        logger_lvl = logging.DEBUG
        logging.basicConfig(
            handlers=[logging.FileHandler('logs/example.log', encoding='utf-8')],
            format='[{asctime:>19}] {filename:<15} {levelname}: {message}',
            style='{',
            datefmt='%d.%m.%Y %H:%M:%S',
            level=logger_lvl
        )
        logger_configured = True
    return logger_configured


logger_configured = False

keys = {
    'vk': 'token_for_vk',
    'vk_confirmation': 'string_for_vk_confirmation',
    'telegram': 'token_for_telegram'
}

db_info = {
    'db': 'db_name',
    'user': 'username',
    'passwd': '***',
    'charset': 'utf8'
}
