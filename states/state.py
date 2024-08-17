from typing import NamedTuple


class State:
    def __init__(self, game):
        self.game = game

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def onExitState(self) -> None:
        pass

    def onEnterState(self, payload: NamedTuple) -> None:
        pass
