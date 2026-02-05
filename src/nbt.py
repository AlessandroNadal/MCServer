import abc
import logging
import struct
from typing import Any, Self

from src.buffer import Buffer
from src.structs import Short, Byte, Int

TAG_END = (0).to_bytes()
INDENT_TEXT = "    "

class TAG(metaclass=abc.ABCMeta):
    id: int
    fmt: str | None = None

    def __init__(self, name: str, value: Any | Self):
        self.name: str = name
        self.value: Any | Self = value

    def to_string(self, indent=0) -> str:
        indent_value = INDENT_TEXT * indent
        s = f"{indent_value}{self.__class__.__name__}(\"{self.name}\")"
        if isinstance(self.value, list):
            s += f"\n{indent_value}{{\n"
            for i in self.value:
                s += f"{i.to_string(indent + 1)}"
            s +=  f"{indent_value}}}\n"
        else:
            s += f": {self.value}\n"

        return s

    def __str__(self) -> str:
        return self.to_string()

    __repr__ = __str__

    def pack(self) -> bytes:
        id_ = self.pack_id()
        name = self.pack_name()
        value = self.pack_value()

        return id_ + name + value

    def pack_id(self) -> bytes:
        return struct.pack(">B", self.id)

    def pack_name(self) -> bytes:
        return self.pack_string(self.name)

    @classmethod
    def unpack(cls, buffer: Buffer, named: bool = True) -> Self:
        return cls(cls.unpack_name(buffer) if named else None, cls.unpack_value(buffer))

    @classmethod
    def unpack_id(cls, buffer: Buffer) -> int:
        return struct.unpack(">B", buffer.read(1))[0]

    @classmethod
    def unpack_name(cls, buffer: Buffer) -> str:
        return TAG.unpack_string(buffer)

    @classmethod
    def unpack_value(cls, buffer: Buffer) -> Any:
        if cls.fmt is not None:
            return struct.unpack(cls.fmt, buffer.read(struct.calcsize(cls.fmt)))[0]

        raise NotImplementedError(f"pack_value not implemented for {cls}")

    def pack_value(self) -> bytes:
        if self.fmt is not None:
            return struct.pack(self.fmt, self.value)
        raise NotImplementedError(f"pack_value not implemented for {self.__class__}")

    @staticmethod
    def pack_string(value: str) -> bytes:
        name = value.encode("utf-8")
        name_length = Short.pack(len(name))

        return name_length + name

    @staticmethod
    def unpack_string(buffer: Buffer) -> str:
        name_length = Short.unpack(buffer)
        return buffer.read(name_length).decode("utf-8")

    def write(self, buffer: Buffer):
        self.write_id(buffer)
        self.write_name(buffer)

    def write_id(self, buffer: Buffer) -> None:
        buffer.write(self.pack_id())

    def write_name(self, buffer: Buffer) -> None:
        buffer.write(self.pack_name())

    def write_value(self, buffer: Buffer) -> None:
        buffer.write(self.pack_value())


# noinspection PyPep8Naming
class TAG_BYTE(TAG):
    id = 0x01
    fmt = ">b"


# noinspection PyPep8Naming
class TAG_SHORT(TAG):
    id = 0x02
    fmt = ">h"


# noinspection PyPep8Naming
class TAG_INT(TAG):
    id = 0x03
    fmt = ">i"


# noinspection PyPep8Naming
class TAG_LONG(TAG):
    id = 0x04
    fmt = ">q"


# noinspection PyPep8Naming
class TAG_FLOAT(TAG):
    id = 0x05
    fmt = ">f"


# noinspection PyPep8Naming
class TAG_DOUBLE(TAG):
    id = 0x06
    fmt = ">d"


# noinspection PyPep8Naming
class TAG_STRING(TAG):
    id = 0x08

    @classmethod
    def unpack_value(cls, buffer: Buffer) -> str:
        return TAG.unpack_string(buffer)

    def pack_value(self) -> bytes:
        return TAG.pack_string(self.value)


# noinspection PyPep8Naming
class TAG_LIST(TAG):
    id = 0x09
    @classmethod
    def unpack_value(cls, buffer: Buffer) -> list[TAG]:
        id_ = buffer.unpack_byte()
        tags = list()
        length = buffer.unpack_int()
        for _ in range(length):
            tags.append(TAGS[id_].unpack(buffer, named=False))
        return tags

    def pack_value(self) -> bytes:

        id_ = Byte.pack(self.id)
        length = Int.pack(len(self.value))
        packed_value = id_ + length
        for tag in self.value:
            packed_value += tag.pack_value()

        return packed_value


# noinspection PyPep8Naming
class TAG_COMPOUND(TAG):
    id = 0x0a



    @classmethod
    def unpack_root(cls, buffer: Buffer):
        if buffer.unpack_byte() != TAG_COMPOUND.id:
            raise ValueError("Buffer must start with TAG_COMPOUND id")

        return cls.unpack(buffer)

    def pack_value(self) -> bytes:
        b = b""

        for tag in self.value:
            b += tag.pack()

        return b + TAG_END

    @classmethod
    def unpack_value(cls, buffer: Buffer) -> list[TAG]:
        value = list()

        while True:
            id_ = buffer.unpack_byte()
            if id_ == 0x00:
                break

            value.append(TAGS[id_].unpack(buffer))

        return value

TAGS: dict[int, type[TAG]] = {
    0x01: TAG_BYTE,
    0x02: TAG_SHORT,
    0x03: TAG_INT,
    0x04: TAG_LONG,
    0x05: TAG_FLOAT,
    0x06: TAG_DOUBLE,
    0x08: TAG_STRING,
    0x09: TAG_LIST,
    0x0a: TAG_COMPOUND
}


# TAGS[0x07] = TAG_BYTEARRAY
# TAGS[0x0b] = TAG_INTARRAY
# TAGS[0x0c] = TAG_LONGARRAY


def print_bytes(bytess: bytes):
    print(bytess)
    print([f"{x:02x}" for x in bytess])


with open("servers.dat", "rb") as f:
    tag = TAG_COMPOUND.unpack_root(Buffer(f.read()))

print(tag)