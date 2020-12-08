import pytest
from botcom import l10n


def test_format():
    result = l10n.format('ru', 'MESSAGE.TEMPLATE', name='name', msg='msg')
    assert result == 'name:\nmsg\n'


def test_wrong_locale():
    result = l10n.format('WRONG LOCALE', 'MESSAGE.TEMPLATE', name='name', msg='msg')
    assert result == 'name:\nmsg\n'


def test_wrong_key():
    with pytest.raises(KeyError):
        l10n.format('', 'WRONG KEY', name='name', msg='msg')


def test_keys():
    required_keys = [
        'MESSAGE.HELP', 'MESSAGE.FULL_HELP', 'MESSAGE.STATUS', 'MESSAGE.NO_RECIPIENT', 'MESSAGE.INVALID_USER',
        'MESSAGE.REGISTER', 'MESSAGE.CONNECTED', 'MESSAGE.CONN_NOTIFICATION', 'MESSAGE.CONN_WAIT',
        'MESSAGE.WAIT_FOR_PARAMS:', 'MESSAGE.NO_SOCIAL', 'MESSAGE.BYE', 'MESSAGE.OFF',
        'MESSAGE.OFF_BLANK', 'MESSAGE.FRIEND_OFF', 'MESSAGE.FRIEND_UNREG', 'MESSAGE.LANG_CHANGED',
        'MESSAGE.UNDEFINED_CMD', 'MESSAGE.WRONG_ARGS', 'MESSAGE.TEMPLATE',
        'BUTTON.NEW_DIALOG:', 'BUTTON.DIALOGS', 'BUTTON.SETTINGS',
        'BUTTON.OFF', 'BUTTON.LANG', 'BUTTON.HELP', 'BUTTON.UNREG', 'BUTTON.START',
        'KEYBOARD.MESSENGERS', 'KEYBOARD.DIALOGS', 'KEYBOARD.SETTINGS', 'KEYBOARD.LANG'
    ]
    for name in l10n.locales:
        for key in required_keys:
            assert key in l10n.locales[name], f'No "{key}" in "{name}" locale'
