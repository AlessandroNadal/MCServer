class Position:
    def __init__(self, x: float, y: float, z: float, yaw: float, pitch: float) -> None:
        self.x = x
        self.y = y
        self.z = z

        self.yaw = yaw
        self.pitch = pitch

    @classmethod
    def from_player_data(cls, player_data: dict):
        position = player_data["pos"]
        return cls(
            position["x"],
            position["y"],
            position["z"],
            position["yaw"],
            position["pitch"],
        )
