from constants import TARGET_FPS
from cutscenes.cutscene1 import Cutscene1
from utils import resource_path
import pygame
import sys
import os

class CutsceneManager():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screenSize = pygame.display.get_window_size()
        fontRelativePath = os.path.join("res", "TTOctosquaresTrialRegular.ttf")
        self.mediumFont = pygame.font.Font(resource_path(fontRelativePath), 50)
        self.largeFont = pygame.font.Font(resource_path(fontRelativePath), 72)
        self.currentFrame = 0

        self.cutscenes = [
            Cutscene1(self)
        ]

    def DisplayCustcene(self, screen, cutsceneId):
        while True:
            if (pygame.event.peek(pygame.QUIT)):
                pygame.quit()
                sys.exit()

            for cutscene in self.cutscenes:
                if (cutscene.id == cutsceneId):
                    cutscene.Draw(screen)

            pygame.display.flip()
            self.clock.tick(TARGET_FPS)
