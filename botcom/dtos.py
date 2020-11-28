from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class User:
    id: str
    name: str
    messenger: str
    nick: str = None
    phone: str = None
    lang: str = None


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
