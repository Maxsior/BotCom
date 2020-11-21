from dataclasses import dataclass


@dataclass
class User:
    id: int
    nick: str
    name: str
    messenger: str


@dataclass
class Message:
    sender: User
    text: str
    attachments: list
