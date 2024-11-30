import io
import logging
from typing import Optional

from twisted.internet import protocol, reactor, endpoints
from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol

from src import Packet
from src.stages.configuration import Configuration
from src.stages.handshake import HandShake
from src.stages.login import Login
from src.stages.status import Status
from src.structs import VarInt

STAGES = {
    -1: HandShake,
    1: Status,
    2: Login,
    4: Configuration
}

logger = logging.getLogger("server")
logging.basicConfig(level=logging.DEBUG)


class Server(Protocol):
    def __init__(self) -> None:
        self.stage = STAGES[-1](self, logger)

    def dataReceived(self, data: bytes) -> None:
        buffer = io.BytesIO(data)
        packet = Packet(initial_bytes=buffer.read(VarInt.unpack(buffer)))
        logger.debug("-" * 20)
        logger.debug(f"Stage: {self.stage.__class__.__name__.title()}")

        next_stage = self.stage.process_packet(packet)
        if next_stage is None:
            return

        self.stage = STAGES[next_stage](self.transport, logger)
        logger.debug(f"Next stage: {self.stage.__class__.__name__.title()}")


class ServerFactory(protocol.Factory):
    def buildProtocol(self, addr: IAddress) -> Optional[Protocol]:
        return Server()


def start(port: int = 25565) -> None:
    logger.info(f"Server started at port {port}")
    endpoints.serverFromString(reactor, f"tcp:{port}").listen(ServerFactory())
    reactor.run()
