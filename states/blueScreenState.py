
import pygame

from states.state import State
from utils import resource_path


class BlueScreenState (State):

    def __init__(self, game):
        super().__init__(game)
        self.background = pygame.image.load(resource_path('./res/blueScreen.png')).convert_alpha()


    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, pygame.Rect(0, 0, 1280, 720))

    def update(self) -> None:
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game.switchState("CreditsState")




