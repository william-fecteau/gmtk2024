from typing import NamedTuple


class InGameStatePayload(NamedTuple):
    world: int
    level: int


class LevelSelectPayload(NamedTuple):
    pass
