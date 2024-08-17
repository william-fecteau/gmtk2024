import sys
from typing import NamedTuple, Optional

import pygame

from constants import SCREEN_SIZE, TARGET_FPS
from states import InGameState, LevelSelectState, MenuState, CreditsState

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF)

        # States
        self.dicStates = {
            InGameState.__name__: InGameState(self),
            MenuState.__name__: MenuState(self),
            LevelSelectState.__name__: LevelSelectState(self),
            CreditsState.__name__: CreditsState(self)
        }
        self.curState = MenuState.__name__
        self.nextState = None
        self.nextStatePayload = None

        self.clock = pygame.time.Clock()

    def gameLoop(self) -> None:
        while True:
            if (pygame.event.peek(pygame.QUIT)):
                pygame.quit()
                sys.exit()

            self.events = pygame.event.get()

            if self.nextState is not None:
                self.dicStates[self.curState].onExitState()
                self.curState = self.nextState
                self.dicStates[self.curState].onEnterState(self.nextStatePayload)
                self.nextState = None
                self.nextStatePayload = None

            self.screen.fill('black')

            self.dicStates[self.curState].update()
            self.dicStates[self.curState].draw(self.screen)

            pygame.display.flip()

            self.clock.tick(TARGET_FPS)

    def switchState(self, newStateStr: str, payload: Optional[NamedTuple] = None) -> None:
        if self.nextState is None and newStateStr in self.dicStates:
            self.nextState = newStateStr
            self.nextStatePayload = payload


if __name__ == "__main__":
    Game().gameLoop()
