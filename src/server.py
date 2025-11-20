import json

from src.player import Player
from src.position import Position


class Server:
    def __init__(self) -> None:
        self.players: set[Player] = set()

        with open("resources/players.json", encoding="utf-8") as f:
            self.stored_players = json.load(f)

    def add_player(self, player: Player) -> None:
        self.players.add(player)

    def sync_player(self, player: Player) -> None:
        player_data = self.stored_players.get(str(player.uuid))
        if player_data is None:
            player.pos = Position(0.0, 0.0, 0.0, -180.0, 0.0)
            return

        player.pos = Position.from_player_data(player_data)

    def player_disconnect(self, player: Player):
        self.stored_players[str(player.uuid)] = {
            "pos": {
                "x": player.pos.x,
                "y": player.pos.y,
                "z": player.pos.z,
                "yaw": player.pos.yaw,
                "pitch": player.pos.pitch
            }
        }

    def save_players(self) -> None:
        for player in self.players:
            if player.pos is None:
                continue

            self.sync_player(player)
            self.stored_players[str(player.uuid)] = {
                "pos": {
                    "x": player.pos.x,
                    "y": player.pos.y,
                    "z": player.pos.z,
                    "yaw": player.pos.yaw,
                    "pitch": player.pos.pitch
                }
            }

        with open("resources/players.json", "w", encoding="utf-8") as f:
            json.dump(self.stored_players, f, indent=4)
