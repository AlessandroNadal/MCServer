from src.structs import UByte


class ChunkSection:


    pass


class Chunk:
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
