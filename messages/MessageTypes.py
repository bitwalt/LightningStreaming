from enum import Enum, auto


class MessageType(Enum):
    HANDSHAKE = auto()
    ASK_MEDIA = auto()
    OK_MEDIA = auto()
    ASK_SWARM = auto()
    SEND_CHUNK = auto()
    PAY_CHUNK =  auto()

    def __str__(self):
        return f'{self.name(self.value)}'
    