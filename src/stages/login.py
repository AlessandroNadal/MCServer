import json
import os
from typing import Callable

from src import Packet
from src.stages.stage import Stage, listen
from src.structs import String, UUID


def pack_registry(packet: Packet, registry_fp: str) -> None:
    with open(registry_fp) as f:
        data: dict[str, dict] = json.load(f)

    for registry_id, registry_data in data.items():
        packet.pack_string(registry_id)
        packet.pack_varint(len(registry_data))

        for entry_id in registry_data.keys():
            packet.pack_string(entry_id)
            packet.pack_bool(False)


class Login(Stage):
    listeners: dict[int, Callable] = dict()

    @listen(0x00)
    def login_start(self, name: String, uuid: UUID):
        login_success = Packet(packet_id=0x02)
        login_success.pack_uuid(uuid)
        login_success.pack_string(name)
        login_success.pack_varint(0)
        login_success.pack_bool(True)

        self.send(login_success)

    @listen(0x03)
    def login_acknowledged(self):
        select_known_packs = Packet(packet_id=0x0E)
        select_known_packs.pack_varint(1)
        select_known_packs.pack_string("minecraft")
        select_known_packs.pack_string("core")
        select_known_packs.pack_string("1.21")
        self.send(select_known_packs)

        for _dir, _, files in os.walk("registries"):
            for file in files:
                registry_data = Packet(packet_id=0x07)
                pack_registry(registry_data, f"{_dir}/{file}")
                self.send(registry_data)
                print(registry_data)

        finish_configuration = Packet(packet_id=0x03)
        self.send(finish_configuration)

        return 4
