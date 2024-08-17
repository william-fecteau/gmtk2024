from typing import NamedTuple


class InGameStatePayload(NamedTuple):
    nbRows: int
    nbColunms: int
    nbAppleOnScreen: int
    nbFrameBeforeNextInput: int
    initialSnakeLength: int

class LevelSelectPayload(NamedTuple):
    world: int
    level: int