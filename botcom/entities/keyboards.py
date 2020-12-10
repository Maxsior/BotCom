from abc import ABC, abstractmethod
import l10n
import entities.buttons as buttons
from entities import User, Button, CommandInfo
import messengers


class Keyboard(ABC):
    def __init__(self, owner: User):
        self.owner = owner

    @property
    @abstractmethod
    def buttons(self):
        raise NotImplementedError


class ConnectKeyboard(Keyboard):
    @property
    def buttons(self):
        if int(self.owner.receiver is None) + len(self.owner.connections) > 1:
            yield buttons.dialogs(self.owner.lang)
            yield
        yield buttons.new_dialog(self.owner.lang)
        yield
        yield buttons.settings(self.owner.lang)
        yield
        if self.owner.receiver is not None:
            yield buttons.off(self.owner.lang)
            yield


class SettingsKeyboard(Keyboard):
    @property
    def buttons(self):
        yield buttons.lang(self.owner.lang)
        yield
        yield buttons.help(self.owner.lang)
        yield
        yield buttons.unreg(self.owner.lang)
        yield


class DialogsKeyboard(Keyboard):
    @property
    def buttons(self):
        connections = self.owner.connections
        print(connections)
        for i, con in enumerate(connections):
            yield Button(
                f'{con.name} ({con.messenger})',
                CommandInfo('chat', [con.messenger, con.id])
            )
            if i % 2 > 0:
                yield
        if len(connections) % 2 != 0:
            yield


class LangKeyboard(Keyboard):
    @property
    def buttons(self):
        for i, lang in enumerate(l10n.locales):
            yield Button(lang, CommandInfo('lang', [lang]))
            if i % 2 > 0:
                yield
        if len(l10n.locales) % 2 != 0:
            yield


class MessengersKeyboard(Keyboard):
    @property
    def buttons(self):
        all_messengers = messengers.get_available_messengers()
        for i, messenger in enumerate(all_messengers):
            yield Button(messenger, CommandInfo('chat', [messenger]))
            if i % 2 > 0:
                yield
        if len(all_messengers) % 2 != 0:
            yield


class StartKeyboard(Keyboard):
    @property
    def buttons(self):
        yield buttons.start(self.owner.lang)
        yield


class EmptyKeyboard(Keyboard):
    @property
    def buttons(self):
        yield from ()
