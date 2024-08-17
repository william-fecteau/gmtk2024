from math import floor

import pygame
import pygame_menu

from constants import (BLACK, EMERALD, GREEN_COLOR, NB_LEVELS, NB_WORLD,
                       SCREEN_SIZE)
from states.payloads import InGameStatePayload
from states.state import State
from utils import resource_path


class LevelSelectState (State):

    def __init__(self, game):
        super().__init__(game)

        width, height = SCREEN_SIZE
        self.surf = pygame.Surface(SCREEN_SIZE)
        self.backgroundSnake = pygame.image.load(resource_path('./res/MenuImg/MenuBackground.png'))
        self.cool_snake = pygame.image.load(resource_path('./res/shnake.png'))
        self.bigSnakeFont = pygame.font.Font(resource_path('./res/SnakeFont.ttf'), 64)
        self.smolSnakeFont = pygame.font.Font(resource_path('./res/SnakeFont.ttf'), 24)

        self.setupMenu()

    def draw(self, screen: pygame.Surface) -> None:
        width, height = SCREEN_SIZE

        background = self.backgroundSnake
        tupleSize = (float(screen.get_width()), float(screen.get_height()))
        newImage = pygame.transform.scale(background, tupleSize)
        self.surf.blit(newImage, (0, 0))

        self.menu.draw(self.surf)

        posMaintext = (float(screen.get_width()/4), float(50))
        self.surf.blit(self.bigSnakeFont.render("Level Selection", True, GREEN_COLOR), posMaintext)

        screen.blit(self.surf, (0, 0))

    def update(self) -> None:
        self.menu.update(self.game.events)

    def goToLevel(self, world: int, level: int) -> None:
        print("world : " + str(world) + " level : " + str(level))
        self.game.switchState(
            "InGameState", InGameStatePayload(world, level)
        )
    def addButtonCalisse(self, world: int, level:int, totalLevelCount: int) -> None:
        print("world : " + str(world) + " level : " + str(level))
        self.menu.add.button("Level" + str(totalLevelCount), lambda: self.goToLevel(world, level))

    def setupMenu(self) -> None:
        width, height = SCREEN_SIZE

        cool_theme = pygame_menu.themes.THEME_GREEN.copy()  # type: ignore
        cool_theme.background_color = BLACK
        cool_theme.widget_font = self.smolSnakeFont
        cool_theme.widget_font_color = EMERALD
        cool_theme.selection_color = GREEN_COLOR
        cool_theme.widget_offset = (0, 200)

        self.menu = pygame_menu.Menu(
            '', width, height, theme=cool_theme, center_content=False, columns=NB_WORLD, rows=NB_LEVELS+1)
        self.menu.get_menubar().hide()

        compteur = 1
        for i in range(NB_WORLD):
            self.menu.add.text_input("Monde " + str(i))
            for j in range(NB_LEVELS):
                self.addButtonCalisse(i, j+1, compteur)
                compteur += 1

    def setRow(self, value: int) -> None:
        self.rows = floor(value)

    def setColumn(self, value: int) -> None:
        self.columns = floor(value)

    def setAppleSpawn(self, value: int) -> None:
        self.appleSpawn = floor(value)

    def setDelay(self, value: int) -> None:
        self.delay = floor(value)
