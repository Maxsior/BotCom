from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    id: str
    nick: str
    phone: str
    name: str
    messenger: str


@dataclass
class Command:
    name: str
    args: List[str]


@dataclass
class Message:
    sender: User
    text: str = ''
    cmd: Command = None
    attachments: List = field(default_factory=list)

