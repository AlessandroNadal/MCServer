import math
from typing import Callable

from src import Packet
from src.chunk import Chunk
from src.stages.stage import Stage, listen
from src.structs import Double, Boolean, Float, Long, VarInt, Byte, UByte, Position, Int


class Play(Stage):
    listeners: dict[int, Callable] = dict()

    def handle_position(self, x: Double, y_feet: Double, z: Double, yaw: Float | None, pitch: Float | None):
        current_chunk_x = math.floor(self.player.pos.x / 16)
        current_chunk_z = math.floor(self.player.pos.z / 16)

        new_chunk_x = math.floor(x / 16)
        new_chunk_z = math.floor(z / 16)

        self.player.pos.x = x
        self.player.pos.y = y_feet
        self.player.pos.z = z
        if yaw is not None and pitch is not None:
            self.player.pos.yaw = yaw
            self.player.pos.pitch = pitch

        if current_chunk_x == new_chunk_x and current_chunk_z == new_chunk_z:
            return

        set_chunk_cache_center = Packet(packet_id=0x57)
        set_chunk_cache_center.pack_varint(new_chunk_x)
        set_chunk_cache_center.pack_varint(new_chunk_z)
        self.send(set_chunk_cache_center)

        min_chunk_x = min(current_chunk_x, new_chunk_x) - 10
        max_chunk_x = max(current_chunk_x, new_chunk_x) + 10

        min_chunk_z = min(current_chunk_z, new_chunk_z) - 10
        max_chunk_z = max(current_chunk_z, new_chunk_z) + 10

        for chunk_x in range(min_chunk_x, max_chunk_x + 1):
            for chunk_z in range(min_chunk_z, max_chunk_z + 1):
                current_chunk_range = (
                        current_chunk_x - 10 <= chunk_x <= current_chunk_x + 10
                        and current_chunk_z - 10 <= chunk_z <= current_chunk_z + 10
                )

                new_chunk_range = (
                        new_chunk_x - 10 <= chunk_x <= new_chunk_x + 10
                        and new_chunk_z - 10 <= chunk_z <= new_chunk_z + 10
                )

                if current_chunk_range and new_chunk_range:
                    continue

                if current_chunk_range and not new_chunk_range:
                    unload_chunk = Packet(packet_id=0x21)
                    unload_chunk.pack_int(chunk_z)
                    unload_chunk.pack_int(chunk_x)
                    self.send(unload_chunk)

                if new_chunk_range:
                    self.send(Chunk.generate_chunk(chunk_x, chunk_z))

    @listen("minecraft:player_abilities")
    def player_abilities(self, flags: Byte) -> None:
        pass

    @listen("minecraft:player_input")
    def player_input(self, flags: UByte) -> None:
        pass

    @listen("minecraft:accept_teleportation")
    def accept_teleportation(self, teleport_id: VarInt):
        pass

    @listen("minecraft:keep_alive")
    def keep_alive(self, payload: Long):
        pass

    @listen("minecraft:client_tick_end")
    def client_tick_end(self):
        pass

    @listen("minecraft:move_player_pos")
    def move_player_pos(self, x: Double, y_feet: Double, z: Double, flags: Byte) -> None:
        self.handle_position(x, y_feet, z, None, None)

    @listen("minecraft:move_player_pos_rot")
    def move_player_pos_rot(
            self,
            x: Double,
            y_feet: Double,
            z: Double,
            yaw: Float,
            pitch: Float,
            flags: Byte):
        self.handle_position(x, y_feet, z, yaw, pitch)

    @listen("minecraft:move_player_rot")
    def move_player_rot(self, yaw: Float, pitch: Float, on_ground: Boolean):
        pass

    @listen("minecraft:move_player_status_only")
    def move_player_status_only(self, flags: Byte):
        pass

    @listen("minecraft:player_action")
    def player_action(self, status: VarInt, location: Position, face: Byte, sequence: VarInt):
        pass

    @listen("minecraft:swing")
    def swing(self):
        pass

    @listen("minecraft:player_loaded")
    def player_loaded(self):
        pass
