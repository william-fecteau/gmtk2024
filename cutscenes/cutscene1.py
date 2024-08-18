import pygame
from constants import GREEN_COLOR, TARGET_FPS
from cutscenes.cutscene import Cutscene

class Cutscene1(Cutscene):
    def __init__(self, manager):
        super().__init__(manager, 0)
        self.currentFrame = 0

    def Draw(self, screen):
        cutsceneScreen = screen.copy()
        cutsceneScreen.fill("black")
        screen.fill("black")

        mainTitle = self.manager.largeFont.render("World 1", True, GREEN_COLOR)
        mainTitlePosX = cutsceneScreen.get_rect().center[0] - (mainTitle.get_rect().width / 2)
        mainTitlePosY = cutsceneScreen.get_rect().center[1] - (mainTitle.get_rect().height / 2)
        mainTitlePos = [mainTitlePosX, mainTitlePosY]
        cutsceneScreen.blit(mainTitle, mainTitlePos)
        
        subTitle = self.manager.mediumFont.render("int 4", True, GREEN_COLOR)
        subTitlePosX = cutsceneScreen.get_rect().center[0] - (subTitle.get_rect().width / 2)
        subTitlePosY = cutsceneScreen.get_rect().center[1] - (subTitle.get_rect().height / 2)
        subTitlePos = [subTitlePosX, subTitlePosY + (mainTitle.get_rect().height / 2) + 10]
        cutsceneScreen.blit(subTitle, subTitlePos)

        scalePercent = (1 / max(1, self.currentFrame / TARGET_FPS / 2))
        scaledSize = [screen.get_rect().width * scalePercent, screen.get_rect().height * scalePercent]
        scaledCutScene = pygame.transform.scale(cutsceneScreen, scaledSize)
        screen.blit(scaledCutScene, (0, self.manager.screenSize[1] - scaledCutScene.get_height()))

        self.currentFrame += 1
