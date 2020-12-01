from dataclasses import dataclass, field, InitVar
from typing import List, Optional
import storage


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

    def __post_init__(self, refine):
        if refine:
            user = storage.Storage().find_user(self.messenger, self.id)
            if user:
                self.key = user.key
                self.lang = user.lang or self.lang
                self.receiver = user.receiver


@dataclass
class CommandInfo:
    name: str
    args: List[str]


@dataclass
class Message:
    text: str = ''
    attachments: List = field(default_factory=list)
    cmd: Optional[CommandInfo] = None
    sender: Optional[User] = None
