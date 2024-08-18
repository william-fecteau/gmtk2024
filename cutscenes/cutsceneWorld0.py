from constants import GREEN_COLOR, LIGHT_BLACK
from cutscenes.cutsceneWorld import CutsceneWorld
import pygame

class CutsceneWorld0(CutsceneWorld):
    def __init__(self, manager):
        super().__init__(manager, 1)

    def Draw(self, screen : pygame.Surface):
        screen.fill(LIGHT_BLACK)

        title : pygame.Surface = self.manager.largeFont.render(self.currentWorldTitle, True, GREEN_COLOR)
        titlePosX = screen.get_rect().center[0] - (title.get_width() / 2)
        titlePosY = screen.get_rect().center[1] - (title.get_height() / 2)
        screen.blit(title, [titlePosX, titlePosY])

        subTitle : pygame.Surface = self.manager.mediumFont.render(self.currentWorldSubTitle, True, GREEN_COLOR)
        subTitlePosX = screen.get_rect().center[0] - (subTitle.get_width() / 2)
        subTitlePosY = screen.get_rect().center[1] - (subTitle.get_height() / 2)
        subTitlePos = [subTitlePosX, subTitlePosY + (title.get_height() / 2) + 10]
        screen.blit(subTitle, subTitlePos)

        seconds = (pygame.time.get_ticks() - self.startTime) / 1000
        self.completed = seconds > 3
