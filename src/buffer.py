"""
Class used for packing and unpacking packets for an easier handling
"""
import io
import string
import struct
import uuid
from typing import Any

from src.structs import (
    UUID,
    Boolean,
    Byte,
    UByte,
    Short,
    UShort,
    String,
    Int,
    Long,
    Double,
    VarInt,
    Position,
    Float, ULong,
)

string_characters = string.ascii_letters + string.digits + ":_"


class Buffer(io.BytesIO):
    """
    Class used for packing and unpacking packets for an easier handling
    """

    def __str__(self) -> str:
        return " ".join([f"{x:02x}" if chr(x) not in string_characters else chr(x) for x in self.getvalue()])

    __repr__ = __str__

    def pack(self, fmt: str, value: Any):
        """
        Packs any value with format fmt
        :param fmt: The struct format to pack
        :param value: The value to pack
        """
        self.write(struct.pack(fmt, value))

    def unpack(self, fmt: str) -> Any:
        """
        Unpack any value given the format fmt
        :param fmt: The format to unpack from
        :return: The struct type of fmt
        """
        return struct.unpack(fmt, self.read(struct.calcsize(fmt)))[0]

    def pack_bool(self, val: bool) -> None:
        """
        Write a boolean to the buffer
        :param val: The boolean to pack
        """
        self.write(Boolean.pack(val))

    def unpack_bool(self) -> bool:
        """
        Unpacks a boolean from the buffer
        :return: The unpacked boolean
        """
        return Boolean.unpack(self)

    def pack_byte(self, val: int) -> None:
        """
        Write The byte to the buffer
        :param val: The byte to pack
        """
        self.write(Byte.pack(val))

    def unpack_byte(self) -> int:
        """
        Unpacks a byte from the buffer
        :return: The unpacked byte
        """
        return Byte.unpack(self)

    def pack_ubyte(self, val: int) -> None:
        """
        Write The ubyte to the buffer
        :param val: The ubyte to pack
        """
        self.write(UByte.pack(val))

    def unpack_ubyte(self) -> int:
        """
        Unpacks an ubyte from the buffer
        :return: The unpacked ubyte
        """
        return UByte.unpack(self)

    def pack_short(self, val: int) -> None:
        """
        Write a short to the buffer
        :param val: The short to pack
        """
        self.write(Short.pack(val))

    def unpack_short(self) -> int:
        """
        Unpacks a short from the buffer
        :return: The unpacked short
        """
        return Short.unpack(self)

    def pack_ushort(self, val: int) -> None:
        """
        Write an ushort to the buffer
        :param val: An ushort to pack
        """
        self.write(UShort.pack(val))

    def unpack_ushort(self) -> int:
        """
        Unpacks an ushort from the buffer
        :return: The unpacked ushort
        """
        return UShort.unpack(self)

    def pack_int(self, val: int) -> None:
        """
        Write an int to the buffer
        :param val: An int to pack
        """
        self.write(Int.pack(val))

    def unpack_int(self) -> int:
        """
        Unpacks an int from the buffer
        :return: The unpacked int
        """
        return Int.unpack(self)

    def pack_long(self, val: int) -> None:
        """
        Write a long to the buffer
        :param val: The long to pack
        """
        self.write(Long.pack(val))

    def unpack_long(self) -> int:
        """
        Unpacks a long from the buffer
        :return: The unpacked long
        """
        return Long.unpack(self)

    def pack_ulong(self, val: int) -> None:
        """
        Write a long to the buffer
        :param val: The ulong to pack
        """
        self.write(ULong.pack(val))

    def unpack_ulong(self) -> int:
        """
        Unpacks a long from the buffer
        :return: The unpacked ulong
        """
        return ULong.unpack(self)

    def pack_float(self, val: float) -> None:
        """
        Write a float to the buffer
        :param val: The float to pack
        """
        self.write(Float.pack(val))

    def unpack_float(self) -> float:
        """
        Unpacks a float from the buffer
        :return: The unpacked float
        """
        return Float.unpack(self)

    def pack_double(self, val: float) -> None:
        """
        Write a double to the buffer
        :param val: The double to pack
        """
        self.write(Double.pack(val))

    def unpack_double(self) -> float:
        """
        Unpacks a double from the buffer
        :return: The unpacked double
        """
        return Double.unpack(self)

    def pack_string(self, val: str) -> None:
        """
        Write a string to the buffer
        :param val: The string to pack
        """
        self.write(String.pack(val))

    def unpack_string(self) -> str:
        """
        Unpacks a string from the buffer
        :return: The unpacked string
        """
        return String.unpack(self)

    def pack_varint(self, val: int) -> None:
        """
        Write a varint to the buffer
        :param val: The varint to pack
        """
        self.write(VarInt.pack(val))

    def unpack_varint(self) -> int:
        """
        Unpacks a varint from the buffer
        :return: The unpacked varint
        """
        return VarInt.unpack(self)

    def pack_position(self, x: int, y: int, z: int) -> None:
        """
        Write The position to the buffer
        :param x: The x position
        :param y: The y position
        :param z: The z position
        """
        self.write(Position.pack((x, y, z)))

    def unpack_position(self) -> tuple[int, int, int]:
        """
        Unpacks a position from the buffer
        :return: The unpacked position
        """
        return Position.unpack(self)

    def pack_uuid(self, _uuid: uuid.UUID) -> None:
        """
        Write a UUID to the buffer
        :param _uuid: The uuid to pack
        """
        self.write(UUID.pack(_uuid))

    def unpack_uuid(self) -> uuid.UUID:
        """
        Unpacks a UUID from the buffer
        :return: The unpacked UUID
        """
        return UUID.unpack(self)

    def pack_bytes(self, data: bytes) -> None:
        """
        Write bytes to the buffer
        :param data: The data to pack
        """
        self.write(data)

    def unpack_bytes(self) -> bytes:
        """
        Unpacks the rest of bytes from the buffer
        :return: The unpacked bytes
        """
        return self.read()
