from constants import TARGET_FPS
from cutscenes.cutsceneWorld import CutsceneWorld
from cutscenes.cutsceneWorld0 import CutsceneWorld0
import pygame

class CutsceneWorld1(CutsceneWorld):
    def __init__(self, manager):
        super().__init__(manager, 1)

    def GetPreviousCutscene(self):
        return CutsceneWorld0(self.manager)

    def DrawCurrentWorld(self, screen: pygame.Surface):
        prevScreenCopy = screen.copy()
        previousCutscene = self.GetPreviousCutscene()
        previousCutscene.Draw(prevScreenCopy)

        scalePercent = max(0.5, (1 / max(1, self.currentStep / TARGET_FPS / 2)))
        scaledSize = [screen.get_width() * scalePercent, screen.get_height() * scalePercent]
        scaledPrevCutscene = pygame.transform.scale(prevScreenCopy, scaledSize)
        screen.blit(scaledPrevCutscene, (0, self.manager.screenSize[1] - scaledPrevCutscene.get_height()))

    def DrawPreviousWorld(self, screen: pygame.Surface):
        pass
