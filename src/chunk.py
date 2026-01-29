"""
Chunk classes and handling
"""
import noise

from src import Packet
from src.buffer import Buffer


class ChunkSection:
    """
    Section of chunk
    """
    pass


scale = 100.0
octaves = 2
persistence = 0.5
lacunarity = 2.0
modifier = 0.2

class Chunk:
    """
    Serialized class of chunk data
    """
    heightmaps = b"\x0a\x00"
    block_entities: int = 0
    sky_light_mask: int = 0
    block_light_mask: int = 0
    empty_sky_light_mask: int = 0,
    empty_block_light_mask: int = 0
    sky_light_array_count: int = 0
    block_light_array_count: int = 0

    def __init__(
            self,
            x: int,
            y: int
    ):
        self.x = x
        self.y = y
        self.data: list[ChunkSection] = list()

        for _ in range(24):
            pass

    @staticmethod
    def generate_chunk(chunk_x: int, chunk_z: int) -> Packet:
        chunk_data = Packet(packet_id=0x27)
        chunk_data.pack_int(chunk_x)
        chunk_data.pack_int(chunk_z)
        chunk_data.pack_varint(0)

        chunk = Buffer()
        heightmaps = list()
        for z in range(chunk_z * 16, chunk_z * 16 + 16):
            l = list()
            for x in range(chunk_x * 16, chunk_x * 16 + 16):
                val = noise.pnoise2(x / scale,
                                    z / scale,
                                    octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=1024,
                                    repeaty=1024,
                                    base=0) * modifier
                val = int(((val + 1) / 2) * 320)
                l.append(val)
            heightmaps.append(l)
        for chunk_y in range(24):
            if chunk_y <= 3:
                chunk.pack_short(4096)

                chunk.pack_ubyte(0)
                chunk.pack_varint(25997)
            else:
                chunk.pack_short(4096)

                chunk.pack_ubyte(4)  # 4 BPE
                chunk.pack_varint(4)  # 2 ENTRIES
                chunk.pack_varint(0)  # AIR
                chunk.pack_varint(9)  # GRASS BLOCK
                chunk.pack_varint(10)  # DIRT
                chunk.pack_varint(6786)  # STONE

                n = 0
                count = 0
                bits_per_entry = 4
                entries_per_long = 64 / bits_per_entry
                for y in range(chunk_y * 16, chunk_y * 16 + 16):
                    for z in range(chunk_z * 16, chunk_z * 16 + 16):
                        for x in range(chunk_x * 16, chunk_x * 16 + 16):
                            entry_id = 3
                            val = heightmaps[z % 16][x % 16]
                            if y > val:
                                entry_id = 0
                            elif y == val:
                                entry_id = 1
                            elif y > val-3:
                                entry_id = 2

                            n |= (entry_id << (bits_per_entry * count))
                            count += 1

                            if count == entries_per_long:
                                chunk.pack_ulong(n)
                                count = 0
                                n = 0
            chunk.pack_ubyte(0)
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

        return chunk_data
