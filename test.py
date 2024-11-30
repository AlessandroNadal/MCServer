from io import BytesIO

from src.structs import VarInt

print(VarInt.unpack(BytesIO(b"\x18")))