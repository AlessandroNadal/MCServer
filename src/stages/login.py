import json
from typing import Callable

from src import Packet
from src.stages.stage import Stage, listen
from src.structs import String, UUID


class Login(Stage):
    listeners: dict[int, Callable] = dict()

    @listen("minecraft:hello")
    def login_start(self, name: String, uuid: UUID):
        login_success = Packet(packet_id=0x02)
        login_success.pack_uuid(uuid)
        login_success.pack_string(name)
        login_success.pack_varint(0)

        self.player.name = name
        self.player.uuid = uuid

        self.server.sync_player(self.player)

        self.send(login_success)

    @listen("minecraft:login_acknowledged")
    def login_acknowledged(self):
        select_known_packs = Packet(packet_id=0x0E)
        select_known_packs.pack_varint(1)
        select_known_packs.pack_string("minecraft")
        select_known_packs.pack_string("core")
        select_known_packs.pack_string("1.21.4")
        self.send(select_known_packs)

        with open("resources/registries-1.21.4.json", encoding="utf-8") as f:
            data = json.load(f)

        for registry_id, registries in data.items():
            registry_data = Packet(packet_id=0x07)
            registry_data.pack_string(registry_id)
            registry_data.pack_varint(len(registries))
            for registry in registries:
                registry_data.pack_string(registry)
                registry_data.pack_bool(False)

            self.send(registry_data)

        tags = Packet(packet_id=0x0D)
        tags.pack_varint(1)
        tags.pack_string("minecraft:worldgen/biome")
        tags.pack_varint(3)
        tags.pack_string("minecraft:is_badlands")
        tags.pack_varint(0)
        tags.pack_string("minecraft:is_jungle")
        tags.pack_varint(0)
        tags.pack_string("minecraft:is_savanna")
        tags.pack_varint(0)
        self.send(tags)
        print(tags)

        finish_configuration = Packet(packet_id=0x03)
        self.send(finish_configuration)

        return 4
