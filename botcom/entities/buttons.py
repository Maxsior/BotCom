from entities import Button, CommandInfo


def new_dialog(lang):
    return Button('BUTTON.NEW_DIALOG', CommandInfo('keyboard', ['messengers'])).localize(lang)


def dialogs(lang):
    return Button('BUTTON.DIALOGS', CommandInfo('keyboard', ['dialogs'])).localize(lang)


def settings(lang):
    return Button('BUTTON.SETTINGS', CommandInfo('keyboard', ['settings'])).localize(lang)


def off(lang):
    return Button('BUTTON.OFF', CommandInfo('off')).localize(lang)


def lang(lang):
    return Button('BUTTON.LANG', CommandInfo('keyboard', ['lang'])).localize(lang)


def help(lang):
    return Button('BUTTON.HELP', CommandInfo('help')).localize(lang)


def unreg(lang):
    return Button('BUTTON.UNREG', CommandInfo('unreg')).localize(lang)


def start(lang):
    return Button('BUTTON.START', CommandInfo('empty')).localize(lang)
