import pytest
from botcom import l10n


def test_format():
    result = l10n.format('ru', 'MSG', name='name', msg='msg')
    assert result == 'name:\nmsg\n'


def test_wrong_locale():
    result = l10n.format('WRONG LOCALE', 'MSG', name='name', msg='msg')
    assert result == 'name:\nmsg\n'


def test_wrong_key():
    with pytest.raises(KeyError):
        l10n.format('', 'WRONG KEY', name='name', msg='msg')


def test_keys():
    required_keys = [
        'HELP', 'FULL_HELP', 'STATUS', 'NO_RECIPIENT', 'INVALID_USER',
        'REGISTER', 'CONNECTED', 'CONN_NOTIFICATION', 'CONN_WAIT',
        'WAIT_FOR_PARAMS', 'NO_SOCIAL', 'BYE', 'OFF', 'OFF_BLANK',
        'FRIEND_OFF', 'UNDEFINED_CMD'
    ]
    for name in l10n.locales:
        for key in required_keys:
            assert key in l10n.locales[name], f'No "{key}" in "{name}" locale'
