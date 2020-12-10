from dataclasses import dataclass, field, InitVar
from typing import List, Optional
import logging
import storage
import l10n


@dataclass
class User:
    id: str
    name: str
    messenger: str
    nick: Optional[str] = None
    phone: Optional[str] = None
    lang: Optional[str] = None
    key: Optional[str] = None
    receiver: Optional[str] = None
    refine: InitVar[bool] = True

    @property
    def registered(self):
        return self.key is not None

    @property
    def connections(self):
        return storage.Storage().get_connected(self.key)

    def __post_init__(self, refine):
        if refine:
            logging.info('Getting user information from database')
            user = storage.Storage().find_user(self.messenger, self.id)
            if user:
                self.key = user.key
                self.lang = user.lang or self.lang
                self.receiver = user.receiver
            logging.info('Done')


@dataclass
class CommandInfo:
    name: str
    args: List[str] = field(default_factory=list)


@dataclass
class Button:
    text: str
    cmd: CommandInfo
    # TODO color

    def localize(self, lang, **kwagrs):
        self.text = l10n.format(lang, self.text, **kwagrs)
        return self


@dataclass
class Message:
    text: str = ''
    attachments: List = field(default_factory=list)
    cmd: Optional[CommandInfo] = None
    sender: Optional[User] = None

    def localize(self, lang, **kwagrs):
        self.text = l10n.format(lang, self.text, **kwagrs)
        return self
