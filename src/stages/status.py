import base64
import json
from typing import Callable

from src import Packet
from src.stages.stage import Stage, listen
from src.structs import Long


def get_status(
        version_name: str = "1.21.1",
        protocol_version: int = 767,
        max_players: int = 100,
        online_players: int = 0,
        image: str = "resources/status.png"
) -> dict:
    with open(image, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
        encoded_image = f"data:image/png;base64,{image_data}"

    status = {
        "version": {
            "name": version_name,
            "protocol": protocol_version
        },
        "players": {
            "max": max_players,
            "online": online_players,
            "sample": [
                {
                    "name": "thinkofdeath",
                    "id": "4566e69f-c907-48ee-8d71-d7ba5aa00d20"
                }
            ]
        },
        "description": {
            "text": "Hello, world!"
        },
        "favicon": encoded_image,
        "enforcesSecureChat": False
    }

    return status


class Status(Stage):
    listeners: dict[int, Callable] = dict()

    @listen(0x00)
    def status_request(self):
        print("STATUS REQUEST")
        response = Packet(packet_id=0x00)
        status_text = json.dumps(get_status())

        response.pack_string(status_text)
        response.send(self.transport)

    @listen(0x01)
    def ping_request(self, timestamp: Long) -> None:
        pong = Packet(packet_id=0x01)
        pong.pack_long(timestamp)
        pong.send(self.transport)
