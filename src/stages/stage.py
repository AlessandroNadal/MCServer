import inspect
from typing import Callable, Any

from twisted.internet.protocol import Protocol

from src.packet import Packet
from src.structs import String, VarInt, UShort


class Stage:
    listeners: dict[int, Callable]

    def __init__(self, transport: Protocol) -> None:
        self.transport = transport

    def process_packet(self, packet: Packet) -> int | None:
        fn = self.listeners.get(packet.id)
        if fn is None:
            print(f"Packet with packet_id: {packet.id} not found")
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
                print(f"Parameter {name} does not have an assigned annotation")
                continue

            params.append(struct_type.unpack(packet))

        return params


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
