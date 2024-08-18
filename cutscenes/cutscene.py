import pygame

class Cutscene():
    def __init__(self, manager, id):
        self.manager = manager
        self.completed = False
        self.id = id

    def Draw(self, screen : pygame.Surface):
        pass

    def IsCompleted(self) -> bool:
        return self.completed
