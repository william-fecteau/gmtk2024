from math import floor

import pygame
import pygame_menu

from constants import BLACK, EMERALD, GREEN_COLOR, SCREEN_SIZE
from states.payloads import InGameStatePayload
from states.state import State
from utils import get_max_levels_per_world, get_max_worlds, resource_path


class LevelSelectState (State):
    def __init__(self, game):
        super().__init__(game)

        self.surf = pygame.Surface(SCREEN_SIZE)
        self.backgroundSnake = pygame.image.load(resource_path('./res/MenuImg/MenuBackground.png'))
        self.cool_snake = pygame.image.load(resource_path('./res/shnake.png'))
        self.bigSnakeFont = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'), 64)
        self.smolSnakeFont = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'), 24)

        self.setupMenu()

    def draw(self, screen: pygame.Surface) -> None:
        background = self.backgroundSnake
        tupleSize = (float(screen.get_width()), float(screen.get_height()))
        newImage = pygame.transform.scale(background, tupleSize)
        self.surf.blit(newImage, (0, 0))

        self.menu.draw(self.surf)

        posMaintext = (float(screen.get_width()/4), float(50))
        self.surf.blit(self.bigSnakeFont.render("Level Selection", True, GREEN_COLOR), posMaintext)

        screen.blit(self.surf, (0, 0))

    def update(self) -> None:
        for event in self.game.events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")
        self.menu.update(self.game.events)

    def goToLevel(self, world: int, level: int) -> None:
        self.game.switchState(
            "InGameState", InGameStatePayload(world, level)
        )

    def addButtonCalisse(self, world: int, level: int, totalLevelCount: int) -> None:
        self.menu.add.button("Level " + str(totalLevelCount), lambda: self.goToLevel(world, level))

    def setupMenu(self) -> None:
        width, height = SCREEN_SIZE

        cool_theme = pygame_menu.themes.THEME_GREEN.copy()  # type: ignore
        cool_theme.background_color = BLACK
        cool_theme.widget_font = self.smolSnakeFont
        cool_theme.widget_font_color = EMERALD
        cool_theme.selection_color = GREEN_COLOR
        cool_theme.widget_offset = (0, 200)

        nb_worlds = get_max_worlds()
        max_nb_rows = max([get_max_levels_per_world(world_num) for world_num in range(nb_worlds)])

        self.menu = pygame_menu.Menu(
            '', width, height, theme=cool_theme, center_content=False, columns=nb_worlds, rows=max_nb_rows+1)
        self.menu.get_menubar().hide()

        level_counter = 1
        for i in range(get_max_worlds()):
            self.menu.add.label("World " + str(i))
            max_levels = get_max_levels_per_world(i)

            for j in range(max_levels):
                self.addButtonCalisse(i, j+1, level_counter)
                level_counter += 1

    def setRow(self, value: int) -> None:
        self.rows = floor(value)

    def setColumn(self, value: int) -> None:
        self.columns = floor(value)

    def setAppleSpawn(self, value: int) -> None:
        self.appleSpawn = floor(value)

    def setDelay(self, value: int) -> None:
        self.delay = floor(value)
