from typing import Callable

from src import Packet
from src.buffer import Buffer
from src.stages.stage import Stage, listen
from src.structs import VarInt, Bytes, String, Byte, Boolean, UByte

SKIN_PART_FLAGS = {
    "Cape": 0x01,
    "Jacket": 0x02,
    "Left sleeve": 0x04,
    "Right sleeve": 0x08,
    "Left Pants Leg": 0x10,
    "Right Pants Leg": 0x20,
    "Hat": 0x40
}


class Configuration(Stage):
    listeners: dict[int, Callable] = dict()

    def generate_chunk(self, x: int, z: int) -> None:
        chunk_data = Packet(packet_id=0x28)
        chunk_data.pack_int(x)
        chunk_data.pack_int(z)
        chunk_data.write(b"\x0A\x00")

        chunk = Buffer()

        for z in range(24):
            chunk.pack_short(4096)

            chunk.pack_ubyte(0)
            chunk.pack_varint(0 if z >= 1 else 2)
            chunk.pack_varint(0)

            chunk.pack_ubyte(0)
            chunk.pack_varint(0)
            chunk.pack_varint(0)

        chunk_data.pack_varint(len(chunk.getvalue()))
        chunk_data.write(chunk.getvalue())

        chunk_data.pack_varint(0)

        chunk_data.pack_byte(0)
        chunk_data.pack_byte(0)
        chunk_data.pack_byte(0)
        chunk_data.pack_byte(0)

        chunk_data.pack_varint(0)
        chunk_data.pack_varint(0)

        self.send(chunk_data)

    @listen("minecraft:client_information")
    def client_information(
            self,
            locale: String,
            view_distance: Byte,
            chat_mode: VarInt,
            chat_colors: Boolean,
            displayed_skin_parts: UByte,
            main_hand: VarInt,
            enable_text_filtering: Boolean,
            allow_server_listings: Boolean,
            particle_status: VarInt
    ):
        self.logger.info("SKIN PARTS")

        for name, flag in SKIN_PART_FLAGS.items():
            self.logger.info(f"\t{name} {"Enabled" if flag & displayed_skin_parts else "Disabled"}")

    @listen("minecraft:custom_payload")
    def custom_payload(self, channel: String, data: Bytes):
        pass

    @listen("minecraft:finish_configuration")
    def finish_configuration(self):
        login_play = Packet(packet_id=0x2C)
        login_play.pack_int(69)
        login_play.pack_bool(False)
        login_play.pack_varint(4)
        login_play.pack_string("minecraft:overworld")
        login_play.pack_string("minecraft:overworld_caves")
        login_play.pack_string("minecraft:the_nether")
        login_play.pack_string("minecraft:the_end")
        login_play.pack_varint(20)
        login_play.pack_varint(10)
        login_play.pack_varint(8)
        login_play.pack_bool(False)
        login_play.pack_bool(False)
        login_play.pack_bool(False)
        login_play.pack_varint(0)
        login_play.pack_string("overworld")
        login_play.pack_long(0)
        login_play.pack_ubyte(1)
        login_play.pack_byte(-1)
        login_play.pack_bool(False)
        login_play.pack_bool(False)
        login_play.pack_bool(False)
        login_play.pack_varint(0)
        login_play.pack_varint(0)
        login_play.pack_bool(False)

        self.send(login_play)


        game_event = Packet(packet_id=0x23)
        game_event.pack_ubyte(13)
        game_event.pack_float(0)
        self.send(game_event)

        for z in range(-10, 11):
            for x in range(-10, 11):
                self.generate_chunk(z, x)

        self.player.spawn()

        return 0

    @listen("minecraft:select_known_packs")
    def select_known_packs(self, count: VarInt, known_packs: Bytes):
        pass
