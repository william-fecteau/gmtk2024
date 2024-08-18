import pygame
from constants import BLACK, GREEN_COLOR, LIGHT_BLACK, TARGET_CUTSCENE_FPS
from cutscenes.cutscene import Cutscene

class CutsceneWorld(Cutscene):
    def __init__(self, manager, currentWorldNumber : int):
        super().__init__(manager, currentWorldNumber)
        self.InitTitles(currentWorldNumber)
        self.animationStartStep = 1.2 * TARGET_CUTSCENE_FPS
        self.animationEndStep = 5 * TARGET_CUTSCENE_FPS
        self.animationSteps = self.animationEndStep - self.animationStartStep
        self.cutsceneEndStep = 7 * TARGET_CUTSCENE_FPS
        self.currentStep = 0

    def InitTitles(self, worldNumber : int):
        self.worldNumber = worldNumber
        self.nextWorldNumber = worldNumber + 1
        worldBits = 2 ** (worldNumber + 1)
        nextWorldBits = 2 ** (self.nextWorldNumber + 1)
        self.currentWorldTitle = "World " + str(worldNumber)
        self.currentWorldSubTitle = str(worldBits) + "-bit Integer"
        self.nextWorldTitle = "World " + str(self.nextWorldNumber)
        self.nextWorldSubTitle = str(nextWorldBits) + "-bit Integer"

    def GetPreviousCutscene(self) -> Cutscene:
        return Cutscene(self.manager, 0) # Must override in children

    def Draw(self, screen : pygame.Surface):
        self.DrawNextWorld(screen)
        self.DrawCurrentWorld(screen)
        self.DrawPreviousWorld(screen)
        self.UpdateTimers()

    def UpdateTimers(self):
        self.currentStep += 1
        self.completed = self.currentStep > self.cutsceneEndStep

    def DrawNextWorld(self, screen : pygame.Surface):
        screenCopy = screen.copy()
        screenCopy.fill(BLACK if (self.nextWorldNumber % 2 == 0) else LIGHT_BLACK)

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

        scalePercent = self.GetScalePercent(2, 1)
        scaledSize = [screen.get_width() * scalePercent, screen.get_height() * scalePercent]
        scaledCutScene = pygame.transform.scale(screenCopy, scaledSize)
        screen.blit(scaledCutScene, (0, self.manager.screenSize[1] - scaledCutScene.get_height()))

    def DrawCurrentWorld(self, screen : pygame.Surface):
        screenCopy = screen.copy()
        screenCopy.fill(BLACK if (self.worldNumber % 2 == 0) else LIGHT_BLACK)

        mainTitle : pygame.Surface = self.manager.largeFont.render(self.currentWorldTitle, True, GREEN_COLOR)
        mainTitlePosX = screenCopy.get_width() / 4 * 3 - (mainTitle.get_width() / 2)
        mainTitlePosY = screenCopy.get_height() / 4 - (mainTitle.get_height() / 2)
        mainTitlePos = [mainTitlePosX, mainTitlePosY]
        screenCopy.blit(mainTitle, mainTitlePos)

        subTitle : pygame.Surface = self.manager.mediumFont.render(self.currentWorldSubTitle, True, GREEN_COLOR)
        subTitlePosX = screenCopy.get_width() / 4 * 3 - (subTitle.get_width() / 2)
        subTitlePosY = screenCopy.get_height() / 4 - (subTitle.get_height() / 2)
        subTitlePos = [subTitlePosX, subTitlePosY + (mainTitle.get_height() / 2) + 10]
        screenCopy.blit(subTitle, subTitlePos)

        scalePercent = self.GetScalePercent(1, 0.5)
        scaledSize = [screen.get_width() * scalePercent, screen.get_height() * scalePercent]
        scaledCutScene = pygame.transform.scale(screenCopy, scaledSize)
        screen.blit(scaledCutScene, (0, self.manager.screenSize[1] - scaledCutScene.get_height()))

    def DrawPreviousWorld(self, screen : pygame.Surface):
        prevScreenCopy = screen.copy()
        previousCutscene = self.GetPreviousCutscene()
        previousCutscene.Draw(prevScreenCopy)

        scalePercent = self.GetScalePercent(0.5, 0.25)
        scaledSize = [screen.get_width() * scalePercent, screen.get_height() * scalePercent]
        scaledPrevCutscene = pygame.transform.scale(prevScreenCopy, scaledSize)
        screen.blit(scaledPrevCutscene, (0, self.manager.screenSize[1] - scaledPrevCutscene.get_height()))

    def GetScalePercent(self, initialScale : float, minScale : float):
        if (self.currentStep < self.animationStartStep):
            return initialScale
        elif (self.currentStep > self.animationEndStep):
            return minScale

        currentAnimationStep = self.currentStep - self.animationStartStep
        progress = currentAnimationStep / self.animationSteps
        return (minScale - initialScale) * progress + initialScale
