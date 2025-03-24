import io
import json
import logging
from typing import Optional

from twisted.internet import protocol, reactor, endpoints, task
from twisted.internet.interfaces import IAddress
from twisted.internet.protocol import Protocol, connectionDone
from twisted.python import failure

from src import Packet
from src.server import Server
from src.stages.configuration import Configuration
from src.stages.handshake import HandShake
from src.stages.login import Login
from src.stages.play import Play
from src.stages.status import Status
from src.structs import VarInt
from src.player import Player

STAGES = {
    -1: HandShake,
    1: Status,
    0: Play,
    2: Login,
    4: Configuration
}

logger = logging.getLogger("server.py")
logging.basicConfig()
logger.setLevel(logging.DEBUG)


class ServerProcess(Protocol):
    def __init__(self, server: Server) -> None:
        self.server = server

        self.player = Player(self)
        self.server.add_player(self.player)

        self.stage = STAGES[-1](self, self.player, self.server, logger)
        self.keep_alive_loop = task.LoopingCall(self.keep_alive)

    def connectionLost(self, reason: failure.Failure = connectionDone) -> None:
        self.server.save_players()

    def dataReceived(self, data: bytes) -> None:
        buffer = io.BytesIO(data)
        packet = Packet(initial_bytes=buffer.read(VarInt.unpack(buffer)))
        if packet.id != 0x0b:
            logger.debug("-" * 20)
            logger.debug(packet)
            logger.debug(f"Stage: {self.stage.__class__.__name__.title()}")

        next_stage = self.stage.process_packet(packet, debug=packet.id != 0x0b)
        if next_stage is None:
            return

        self.stage = STAGES[next_stage](self, self.player, self.server, logger)
        if next_stage == 0:
            self.keep_alive_loop.start(15)
        logger.debug(f"Next stage: {self.stage.__class__.__name__.title()}")

    def keep_alive(self) -> None:
        keep_alive_packet = Packet(packet_id=0x27)
        keep_alive_packet.pack_long(0)
        self.stage.send(keep_alive_packet)


class ServerFactory(protocol.Factory):
    def __init__(self) -> None:
        self.server = Server()

    def buildProtocol(self, addr: IAddress) -> Optional[Protocol]:
        return ServerProcess(self.server)


def start(port: int = 25565) -> None:
    logger.info(f"Server started at port {port}")
    endpoints.serverFromString(reactor, f"tcp:{port}").listen(ServerFactory())
    reactor.run()
