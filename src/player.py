import twisted.internet.protocol

from src import Packet
from src.position import Position


class Player:
    def __init__(self, protocol: twisted.internet.protocol.Protocol) -> None:
        self.protocol = protocol

        self.name = None
        self.uuid = None

        self.pos: Position | None = None

    def __str__(self):
        return f"Player({self.name=}, {self.uuid=}, {self.pos=}"

    def spawn(self):
        if self.pos is None:
            raise Exception("Player is not syncronized yet")

        player_position = Packet(packet_id=0x41)
        player_position.pack_varint(69)
        player_position.pack_double(self.pos.x)
        player_position.pack_double(self.pos.y)
        player_position.pack_double(self.pos.z)
        player_position.pack_double(0)
        player_position.pack_double(0)
        player_position.pack_double(0)
        player_position.pack_float(self.pos.yaw)
        player_position.pack_float(self.pos.pitch)
        player_position.pack_int(0)
        player_position.send(self.protocol)

    def send_message(self, text: str) -> None:
        message = Packet(packet_id=0x77)

