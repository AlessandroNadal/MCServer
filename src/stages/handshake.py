from typing import Callable

from src.stages.stage import Stage, listen
from src.structs import VarInt, String, UShort


class HandShake(Stage):
    listeners: dict[int, Callable] = dict()

    @listen(0)
    def foo(self, protocol_version: VarInt, host: String, port: UShort, next_state: VarInt):
        print(protocol_version + 1)
        print(f"{protocol_version=}")
        print(f"{host=}")
        print(f"{port=}")
        print(f"{next_state=}")
        return next_state
