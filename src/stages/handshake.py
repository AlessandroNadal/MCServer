from typing import Callable

from src.stages.stage import Stage, listen
from src.structs import VarInt, String, UShort


class HandShake(Stage):
    listeners: dict[int, Callable] = dict()

    @listen(0x00)
    def intention(self, protocol_version: VarInt, host: String, port: UShort, next_state: VarInt):
        return next_state
