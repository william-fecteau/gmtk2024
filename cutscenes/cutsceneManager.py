from cutscenes.cutsceneWorld0 import CutsceneWorld0
from cutscenes.cutsceneWorld1 import CutsceneWorld1
from cutscenes.cutsceneWorldOther import CutsceneWorldOther
from constants import TARGET_CUTSCENE_FPS
from utils import resource_path
import pygame
import sys
import os

class CutsceneManager():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screenSize = pygame.display.get_window_size()
        fontRelativePath = os.path.join("res", "TTOctosquaresTrialRegular.ttf")
        self.mediumFont = pygame.font.Font(resource_path(fontRelativePath), 60)
        self.largeFont = pygame.font.Font(resource_path(fontRelativePath), 100)
        self.skipCutscenes = False
        self.currentFrame = 0

    def DisplayCustcene(self, screen : pygame.Surface, cutsceneId : int):
        if (self.skipCutscenes):
            return

        match (cutsceneId):
            case 0: cutscene = CutsceneWorld0(self)
            case 1: cutscene = CutsceneWorld1(self)
            case _: cutscene = CutsceneWorldOther(self, cutsceneId)

        while True:
            if (pygame.event.peek(pygame.QUIT)):
                pygame.quit()
                sys.exit()

            if (cutscene.IsCompleted()):
                return

            cutscene.Draw(screen)

            pygame.display.flip()
            self.clock.tick(TARGET_CUTSCENE_FPS)
