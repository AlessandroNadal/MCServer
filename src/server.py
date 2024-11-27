import io
from typing import Optional

from twisted.internet import protocol, reactor, endpoints
from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol

from src import Packet
from src.stages.handshake import HandShake
from src.stages.status import Status
from src.structs import VarInt

STAGES = {
    -1: HandShake,
    1: Status
}


class Server(Protocol):
    def __init__(self) -> None:
        self.stage = STAGES[-1](self)

    def dataReceived(self, data: bytes) -> None:
        buffer = io.BytesIO(data)
        packet = Packet(initial_bytes=buffer.read(VarInt.unpack(buffer)))
        print("-"*20)
        print(self.stage.__class__.__name__)
        next_stage = self.stage.process_packet(packet)
        if next_stage is None:
            return
        print(next_stage)
        self.stage = STAGES[next_stage](self.transport)


class ServerFactory(protocol.Factory):
    def buildProtocol(self, addr: IAddress) -> Optional[Protocol]:
        return Server()


def start() -> None:
    print("Server started")
    endpoints.serverFromString(reactor, "tcp:25565").listen(ServerFactory())
    reactor.run()
    print("Exiting server")
