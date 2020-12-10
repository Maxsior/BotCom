from entities import Button, CommandInfo


new_dialog = lambda lang: Button('BUTTON.NEW_DIALOG', CommandInfo('keyboard', ['messengers'])).localize(lang)
dialogs = lambda lang: Button('BUTTON.DIALOGS', CommandInfo('keyboard', ['dialogs'])).localize(lang)
settings = lambda lang: Button('BUTTON.SETTINGS', CommandInfo('keyboard', ['settings'])).localize(lang)
off = lambda lang: Button('BUTTON.OFF', CommandInfo('off')).localize(lang)

lang = lambda lang: Button('BUTTON.LANG', CommandInfo('keyboard', ['lang'])).localize(lang)
help = lambda lang: Button('BUTTON.HELP', CommandInfo('help')).localize(lang)
unreg = lambda lang: Button('BUTTON.UNREG', CommandInfo('unreg')).localize(lang)

start = lambda lang: Button('BUTTON.START', CommandInfo('empty')).localize(lang)
