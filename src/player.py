import twisted.internet.protocol

from src import Packet
from src.position import Position


class Player:
    def __init__(self, protocol: twisted.internet.protocol.Protocol) -> None:
        self.protocol = protocol

        self.name = None
        self.uuid = None

        self.pos: Position | None = None

    def spawn(self):
        if self.pos is None:
            raise Exception("Player is not syncronized yet")

        print(self.pos.__dict__)
        player_position = Packet(packet_id=0x42)
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

