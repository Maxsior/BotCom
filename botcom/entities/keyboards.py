import abc
import l10n
import entities.buttons as buttons
from entities import User, Button, CommandInfo


class Keyboard(abc.ABC):
    def __init__(self, owner: User):
        self.owner = owner

    @abc.abstractmethod
    @property
    def buttons(self):
        raise NotImplementedError

    def localize(self, lang: str):
        for button in self.buttons:
            if button:
                button.text = l10n.format(lang, button.text)


class ConnectKeyboard(Keyboard):
    @property
    def buttons(self):
        if len(self.owner.connections) > 1:
            yield buttons.dialogs
            yield
        yield buttons.new_dialog
        yield
        yield buttons.settings
        if self.owner.receiver is not None:
            yield
            yield buttons.off


class SettingsKeyboard(Keyboard):
    @property
    def buttons(self):
        yield buttons.lang
        yield
        yield buttons.help
        yield
        yield buttons.unreg


class DialogsKeyboard(Keyboard):
    @property
    def buttons(self):
        connections = self.owner.connections
        for i, con in enumerate(connections):
            yield Button(f'{con.name} ({con.messenger})', CommandInfo('chat', [con.messenger, con.id]))
            if i % 2 > 0:
                yield


class LangsKeyboard(Keyboard):
    @property
    def buttons(self):
        for i, lang in enumerate(l10n.locales):
            yield Button(lang, CommandInfo('lang', [lang]))
            if i % 2 > 0:
                yield


class MessengersKeyboard(Keyboard):
    @property
    def buttons(self):
        # all_messengers = Messenger.get_available_messengers()
        # for i, messenger in enumerate(all_messengers):
        # TODO handle clicks on messengers buttons
        yield from ()


class StartKeyboard(Keyboard):
    def buttons(self):
        yield buttons.start


class EmptyKeyboard(Keyboard):
    def buttons(self):
        yield from ()
