
import pygame

from constants import SCREEN_SIZE
from grid import Grid
from states.payloads import InGameStatePayload

from .state import State


class InGameState(State):
    CELL_SIZE = 32

    def __init__(self, game):
        super().__init__(game)

    def update(self) -> None:
        for event in self.game.events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")

        self.curFrame += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.lastDir[0] != 1:
            self.grid.direction = (-1, 0)
        elif keys[pygame.K_DOWN] and self.lastDir[0] != -1:
            self.grid.direction = (1, 0)
        elif keys[pygame.K_RIGHT] and self.lastDir[1] != -1:
            self.grid.direction = (0, 1)
        elif keys[pygame.K_LEFT] and self.lastDir[1] != 1:
            self.grid.direction = (0, -1)

        if self.curFrame % self.nbFrameBeforeNextInput == 0:
            self.grid.update()

            if self.grid.isDead:
                self.game.switchState("MenuState")

            self.lastDir = self.grid.direction

    def draw(self, screen) -> None:
        board = pygame.Surface((self.grid.nbColumns * self.CELL_SIZE, self.grid.nbRows * self.CELL_SIZE))
        boardRect = board.get_rect()
        tile = pygame.Surface((InGameState.CELL_SIZE, InGameState.CELL_SIZE))

        for i in range(self.grid.nbRows):
            for j in range(self.grid.nbColumns):
                if self.grid.grid[i, j] == Grid.EMPTY:
                    variant = True
                    if i % 2 == 0:
                        variant = not variant
                    if j % 2 == 0:
                        variant = not variant

                    if variant:
                        tile.fill((48, 48, 48))
                    else:
                        tile.fill((36, 36, 36))
                elif self.grid.grid[i, j] == Grid.HEAD or self.grid.grid[i, j] == Grid.BODY:
                    tile.fill("green")
                elif self.grid.grid[i, j] == Grid.WALL:
                    tile.fill("black")
                elif self.grid.grid[i, j] == Grid.APPLE:
                    tile.fill("red")

                board.blit(tile, (j * InGameState.CELL_SIZE, i * InGameState.CELL_SIZE))

        boardRect.center = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
        screen.blit(board, boardRect)

    def onEnterState(self, payload: InGameStatePayload) -> None:
        self.grid = Grid(payload.nbRows + 2, payload.nbColunms + 2, payload.nbAppleOnScreen, payload.initialSnakeLength)
        self.nbFrameBeforeNextInput = payload.nbFrameBeforeNextInput
        self.curFrame = 0

    def onExitState(self) -> None:
        pass
