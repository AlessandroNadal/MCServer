from typing import Callable

import noise

from src import Packet
from src.buffer import Buffer
from src.chunk import Chunk
from src.enums import GameEvent
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
        login_play = Packet(packet_id=0x2B)
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

        game_event = Packet(packet_id=0x22)
        game_event.pack_ubyte(GameEvent.START_WAITING_FOR_LEVEL_CHUNKS)
        game_event.pack_float(0)

        self.send(game_event)

        for z in range(-12, 13):
            for x in range(-12, 13):
                self.send(Chunk.generate_chunk(x, z))

        self.player.spawn()

        return 0

    @listen("minecraft:select_known_packs")
    def select_known_packs(self, count: VarInt, known_packs: Bytes):
        pass
