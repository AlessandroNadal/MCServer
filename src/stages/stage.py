import inspect
import json
from logging import Logger
from typing import Callable, Any

from twisted.internet.protocol import Protocol

from src.packet import Packet
from src.player import Player
from src.server import Server

with open("resources/packets.json") as f:
    packets = json.load(f)


class Stage:
    listeners: dict[int, Callable]

    def __init__(self, protocol: Protocol, player: Player, server: Server, logger: Logger) -> None:
        self.logger = logger
        self.player = player
        self.server = server
        self.protocol = protocol

    def process_packet(self, packet: Packet, debug: bool = False) -> int | None:
        description = list(
            filter(
                lambda p: p[1]["protocol_id"] == packet.id,
                packets[self.__class__.__name__.lower()]["serverbound"].items(),
            )
        )[0][0]
        if debug:
            self.logger.debug(f"Packet ID: {hex(packet.id)} {description}")
        fn = self.listeners.get(packet.id)
        if fn is None:
            self.logger.warning(f"Packet with packet_id: {hex(packet.id)} not found")
            return

        args = self.decode_args(packet)
        return fn(self, *args)

    def decode_args(self, packet: Packet) -> list[Any]:
        signature = inspect.signature(self.listeners[packet.id])
        params = list()
        for name, struct in signature.parameters.items():
            if name == "self":
                continue

            struct_type = struct.annotation
            if struct_type == inspect.Parameter.empty:
                self.logger.warning(f"Parameter {name} does not have an assigned annotation")
                continue

            val: Any = struct_type.unpack(packet)

            params.append(val)
            self.logger.debug(f"{name}: {val}")

        return params

    def send(self, packet: Packet) -> None:
        packet.send(self.protocol)


class listen_wrap:
    def __init__(self, packet_id: int, fn: Callable, owner: Stage = None) -> None:
        self.packet_id = packet_id
        self.fn = fn
        self.owner = owner

    def __set_name__(self, owner, name):
        self.owner = owner
        self.owner.listeners[self.packet_id] = self.fn

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


def listen(packet_id: int):
    return lambda func: listen_wrap(packet_id, func)
