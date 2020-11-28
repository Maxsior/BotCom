from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    id: str
    name: str
    messenger: str
    nick: str = None
    phone: str = None


@dataclass
class CommandInfo:
    name: str
    args: List[str]


@dataclass
class Message:
    sender: User
    text: str = ''
    cmd: CommandInfo = None
    attachments: List = field(default_factory=list)
