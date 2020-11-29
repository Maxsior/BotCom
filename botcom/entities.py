from dataclasses import dataclass, field
from typing import List, Optional
from storage import Storage


@dataclass
class User:
    id: str
    name: str
    messenger: str
    nick: Optional[str] = None
    phone: Optional[str] = None
    lang: Optional[str] = None
    key: Optional[str] = field(init=False, default=None)
    receiver: Optional[str] = field(init=False, default=None)

    @property
    def is_registered(self):
        return self.key is not None

    def __post_init__(self):
        user = Storage().find_user(self.messenger, self.id)
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
