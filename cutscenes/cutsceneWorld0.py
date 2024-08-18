from constants import LIGHT_BLACK, TARGET_CUTSCENE_FPS, WHITE, WORLD_COLORS
from cutscenes.cutsceneWorld import CutsceneWorld
import pygame

class CutsceneWorld0(CutsceneWorld):
    def __init__(self, manager):
        super().__init__(manager, 1)

    def Draw(self, screen : pygame.Surface):
        screen.fill(LIGHT_BLACK)
        textColor = WORLD_COLORS.get(0, WHITE)

        title : pygame.Surface = self.manager.largeFont.render(self.currentWorldTitle, True, textColor)
        titlePosX = screen.get_rect().center[0] - (title.get_width() / 2)
        titlePosY = screen.get_rect().center[1] - (title.get_height() / 2)
        screen.blit(title, [titlePosX, titlePosY])

        subTitle : pygame.Surface = self.manager.mediumFont.render(self.currentWorldSubTitle, True, textColor)
        subTitlePosX = screen.get_rect().center[0] - (subTitle.get_width() / 2)
        subTitlePosY = screen.get_rect().center[1] - (subTitle.get_height() / 2)
        subTitlePos = [subTitlePosX, subTitlePosY + (title.get_height() / 2) + 10]
        screen.blit(subTitle, subTitlePos)

        self.currentStep += 1
        self.completed = self.currentStep > 2.5 * TARGET_CUTSCENE_FPS
