from typing import Callable

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

    @listen(0x00)
    def client_information(
            self,
            locale: String,
            view_distance: Byte,
            chat_mode: VarInt,
            chat_colors: Boolean,
            displayed_skin_parts: UByte,
            main_hand: VarInt,
            enable_text_filtering: Boolean,
            allow_server_listings: Boolean
    ):
        self.logger.info("SKIN PARTS")

        for name, flag in SKIN_PART_FLAGS.items():
            self.logger.info(f"\t{name} {"Enabled" if flag & displayed_skin_parts else "Disabled"}")

    @listen(0x02)
    def custom_payload(self, channel: String, data: Bytes):
        pass

    @listen(0x03)
    def finish_configuration(self):
        return 0

    @listen(0x07)
    def select_known_packs(self, count: VarInt, known_packs: Bytes):
        pass
