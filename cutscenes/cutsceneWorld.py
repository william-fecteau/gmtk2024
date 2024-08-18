import pygame
from constants import BLACK, GREEN_COLOR, LIGHT_BLACK, TARGET_FPS
from cutscenes.cutscene import Cutscene

class CutsceneWorld(Cutscene):
    def __init__(self, manager, currentWorldNumber : int):
        super().__init__(manager)
        self.InitTitles(currentWorldNumber)
        self.currentStep = 0

    def InitTitles(self, worldNumber : int):
        nextWorldNumber = worldNumber + 1
        worldBits = 2 ** (worldNumber + 1)
        nextWorldBits = 2 ** (nextWorldNumber + 1)
        self.currentWorldTitle = "World " + str(worldNumber)
        self.currentWorldSubTitle = str(worldBits) + "-bit Integer"
        self.nextWorldTitle = "World " + str(nextWorldNumber)
        self.nextWorldSubTitle = str(nextWorldBits) + "-bit Integer"

    def SetStep(self, step : int):
        self.currentStep = step

    def Draw(self, screen : pygame.Surface):
        self.DrawNextWorld(screen)
        self.DrawCurrentWorld(screen)
        self.currentStep += 1

    def DrawNextWorld(self, screen : pygame.Surface):
        screenCopy = screen.copy()
        screenCopy.fill(BLACK)

        mainTitle : pygame.Surface = self.manager.largeFont.render(self.nextWorldTitle, True, GREEN_COLOR)
        mainTitlePosX = screenCopy.get_width() / 4 * 3 - (mainTitle.get_width() / 2)
        mainTitlePosY = screenCopy.get_height() / 4 - (mainTitle.get_height() / 2)
        mainTitlePos = [mainTitlePosX, mainTitlePosY]
        screenCopy.blit(mainTitle, mainTitlePos)

        subTitle : pygame.Surface = self.manager.mediumFont.render(self.nextWorldSubTitle, True, GREEN_COLOR)
        subTitlePosX = screenCopy.get_width() / 4 * 3 - (subTitle.get_width() / 2)
        subTitlePosY = screenCopy.get_height() / 4 - (subTitle.get_height() / 2)
        subTitlePos = [subTitlePosX, subTitlePosY + (mainTitle.get_height() / 2) + 10]
        screenCopy.blit(subTitle, subTitlePos)

        scalePercent = max(1, (2 / max(1, self.currentStep / TARGET_FPS / 2)))
        scaledSize = [screen.get_width() * scalePercent, screen.get_height() * scalePercent]
        scaledCutScene = pygame.transform.scale(screenCopy, scaledSize)
        screen.blit(scaledCutScene, (0, self.manager.screenSize[1] - scaledCutScene.get_height()))

    def DrawCurrentWorld(self, screen : pygame.Surface):
        screenCopy = screen.copy()
        screenCopy.fill(LIGHT_BLACK)

        mainTitle : pygame.Surface = self.manager.largeFont.render(self.currentWorldTitle, True, GREEN_COLOR)
        mainTitlePosX = screenCopy.get_rect().center[0] - (mainTitle.get_width() / 2)
        mainTitlePosY = screenCopy.get_rect().center[1] - (mainTitle.get_height() / 2)
        mainTitlePos = [mainTitlePosX, mainTitlePosY]
        screenCopy.blit(mainTitle, mainTitlePos)

        subTitle : pygame.Surface = self.manager.mediumFont.render(self.currentWorldSubTitle, True, GREEN_COLOR)
        subTitlePosX = screenCopy.get_rect().center[0] - (subTitle.get_width() / 2)
        subTitlePosY = screenCopy.get_rect().center[1] - (subTitle.get_height() / 2)
        subTitlePos = [subTitlePosX, subTitlePosY + (mainTitle.get_height() / 2) + 10]
        screenCopy.blit(subTitle, subTitlePos)

        scalePercent = max(0.5, (1 / max(1, self.currentStep / TARGET_FPS / 2)))
        scaledSize = [screen.get_width() * scalePercent, screen.get_height() * scalePercent]
        scaledCutScene = pygame.transform.scale(screenCopy, scaledSize)
        screen.blit(scaledCutScene, (0, self.manager.screenSize[1] - scaledCutScene.get_height()))
