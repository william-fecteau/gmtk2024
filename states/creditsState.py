from constants import TARGET_FPS
from states.menuState import MenuState
from states.state import State
from typing import NamedTuple
from random import randint
import pygame
import utils
import os

class CreditsState(State):
    def __init__(self, game):
        super().__init__(game)
        self.currentFrame = 0
        self.gamers = []

        gamersDirectoryPath = utils.resource_path(os.path.join("res", "credits"))
        gamersDirectory = os.fsencode(gamersDirectoryPath)
        gamerNames = []
    
        for file in os.listdir(gamersDirectory):
            filename = os.fsdecode(file)
            gamerName = filename.split("_")[0]

            if (gamerName not in gamerNames):
                gamerNames.append(gamerName)
                self.gamers.append(Gamer(len(self.gamers), gamerName))

    def onEnterState(self, payload: NamedTuple) -> None:
        pass
    
    def update(self) -> None:
        for event in self.game.events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState(MenuState.__name__)
        
        for gamer in self.gamers:
            gamer.Update(self.currentFrame)

        self.currentFrame += 1

    def draw(self, screen) -> None:
        for gamer in self.gamers:
            gamer.Draw(screen)

    def onExitState(self) -> None:
        pass

class Gamer:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.sprites = self.LoadSprites()
        self.updateFrame = randint(0, TARGET_FPS)
        self.animationIndex = randint(0, len(self.sprites) - 1)
        self.screenSize = pygame.display.get_window_size()

    def LoadSprites(self):
        spritesDirectory = utils.resource_path(os.path.join("res", "credits"))
        spritesPrefix =  self.name.lower() + "_"
        spritePath = os.path.join(spritesDirectory, spritesPrefix)
        sprites = []

        spriteIndex = 0
        spriteName = spritePath + str(spriteIndex) + ".png"

        while (os.path.isfile(spriteName)):
            sprites.append(pygame.image.load(spriteName).convert_alpha())
            spriteIndex += 1
            spriteName = spritePath + str(spriteIndex) + ".png"

        return sprites

    def Update(self, currentFrame):
        if (currentFrame % TARGET_FPS == self.updateFrame):
            self.animationIndex = (self.animationIndex + 1) % len(self.sprites) 

    def Draw(self, screen):
        paddingTop = self.screenSize[1] / 32
        currentSprite = self.sprites[self.animationIndex]
        posX = self.screenSize[0] / 3 * (self.id % 3) + 30
        posY = self.screenSize[1] / 4 * (self.id // 3) + paddingTop
        screen.blit(currentSprite, pygame.Rect(posX, posY, 128, 128))
