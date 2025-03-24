import string

from twisted.internet.protocol import Protocol

from src.buffer import Buffer
from src.structs import VarInt

string_characters = string.ascii_letters + string.digits + ":_"


class Packet(Buffer):
    def __init__(self, *, packet_id: int = None, initial_bytes=None) -> None:

        if packet_id is None and initial_bytes is None:
            raise NotImplementedError("You need to pass packet_id or initial_bytes")

        if packet_id is None:
            super().__init__(initial_bytes)
            self.id = self.unpack_varint()
        else:
            super().__init__()
            self.id = packet_id
            self.pack_varint(packet_id)

    def send(self, protocol: Protocol):
        protocol.transport.write(VarInt.pack(len(self.getvalue())) + self.getvalue())

    def __str__(self) -> str:
        return " ".join([f"{x:02x}" if chr(x) not in string_characters else chr(x) for x in self.getvalue()])
