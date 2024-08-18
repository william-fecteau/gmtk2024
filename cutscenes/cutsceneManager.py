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
        self.currentFrame = 0

        self.skipCutscenes = False
        self.cutscenePlayed = True
        self.queuedCutscene = -1

    def QueueCutscene(self, cutsceneId : int):
        self.queuedCutscene = cutsceneId
        self.cutscenePlayed = cutsceneId < 0

    def DisplayCustcene(self, screen : pygame.Surface):
        if (self.skipCutscenes or self.cutscenePlayed):
            return

        match (self.queuedCutscene):
            case 0: cutscene = CutsceneWorld0(self)
            case 1: cutscene = CutsceneWorld1(self)
            case _: cutscene = CutsceneWorldOther(self, self.queuedCutscene)

        while True:
            if (pygame.event.peek(pygame.QUIT)):
                pygame.quit()
                sys.exit()

            for event in pygame.event.get():
                if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                    self.cutscenePlayed = True
                    return

            if (cutscene.IsCompleted()):
                self.cutscenePlayed = True
                return

            cutscene.Draw(screen)

            pygame.display.flip()
            self.clock.tick(TARGET_CUTSCENE_FPS)
