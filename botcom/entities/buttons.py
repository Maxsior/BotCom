from entities import Button, CommandInfo

new_dialog = Button('BUTTONS.NEW_DIALOG', CommandInfo('keyboard', ['messengers']))
dialogs = Button('BUTTONS.DIALOGS', CommandInfo('keyboard', ['dialogs']))
settings = Button('BUTTONS.SETTINGS', CommandInfo('keyboard', ['settings']))
off = Button('BUTTONS.OFF', CommandInfo('off'))


lang = Button('BUTTONS.LANG', CommandInfo('keyboard', ['lang']))
help = Button('BUTTONS.HELP', CommandInfo('help'))
unreg = Button('BUTTONS.UNREG', CommandInfo('unreg'))

start = Button('BUTTONS.START', CommandInfo('empty'))
