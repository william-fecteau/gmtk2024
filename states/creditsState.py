from constants import GREEN_COLOR, TARGET_FPS
from states.menuState import MenuState
from utils import resource_path
from states.state import State
from random import randint, shuffle
import pygame
import os

class CreditsState(State):
    def __init__(self, game):
        super().__init__(game)

        fontRelativePath = os.path.join("res", "TTOctosquaresTrialRegular.ttf")
        self.font = pygame.font.Font(resource_path(fontRelativePath), 40)
        self.screenSize = pygame.display.get_window_size()
        self.currentFrame = 0
        self.gamers = []

        gamersDirectoryPath = resource_path(os.path.join("res", "credits"))
        gamersDirectory = os.fsencode(gamersDirectoryPath)
        gamerNames = []

        for file in os.listdir(gamersDirectory):
            filename = os.fsdecode(file)
            gamerName = filename.split("_")[0]

            if (gamerName not in gamerNames):
                gamerNames.append(gamerName)
                self.gamers.append(Gamer(self, gamerName))

    def onEnterState(self, payload) -> None:
        shuffle(self.gamers)

        for gamer in self.gamers:
            gamer.UpdateRandoms()

    def update(self) -> None:
        for event in self.game.events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState(MenuState.__name__)

        for gamer in self.gamers:
            gamer.Update(self.currentFrame)

        self.currentFrame += 1

    def draw(self, screen) -> None:
        for i in range(0, len(self.gamers)):
            self.gamers[i].Draw(screen, i)

class Gamer:
    def __init__(self, state, name) -> None:
        self.name = name
        self.state = state
        self.sprites = self.LoadSprites()

    def LoadSprites(self):
        spritesPrefix = self.name + "_"
        spritesDirectory = resource_path(os.path.join("res", "credits"))
        spritePath = os.path.join(spritesDirectory, spritesPrefix)
        sprites = []

        spriteIndex = 0
        spriteName = spritePath + str(spriteIndex) + ".png"

        while (os.path.isfile(spriteName)):
            sprites.append(pygame.image.load(spriteName).convert_alpha())
            spriteIndex += 1
            spriteName = spritePath + str(spriteIndex) + ".png"

        return sprites

    def UpdateRandoms(self):
        self.updateFrame = randint(0, TARGET_FPS - 1)
        self.animationIndex = randint(0, len(self.sprites) - 1)

    def Update(self, currentFrame):
        if (currentFrame % TARGET_FPS == self.updateFrame):
            self.animationIndex = (self.animationIndex + 1) % len(self.sprites)

    def Draw(self, screen, positionId):
        posX = self.state.screenSize[0] / 3 * (positionId % 3)
        posY = self.state.screenSize[1] / 4 * (positionId // 3)
        self.DrawLogo(screen, posX, posY)
        self.DrawName(screen, posX, posY)

    def DrawLogo(self, screen, posX, posY):
        paddingTop = self.state.screenSize[1] / 32
        currentSprite = self.sprites[self.animationIndex]
        screen.blit(currentSprite, pygame.Rect(posX + 30, posY + paddingTop, 128, 128))

    def DrawName(self, screen, posX, posY):
        position = (posX + 175, posY + self.state.screenSize[1] / 32 + 45)
        screen.blit(self.state.font.render(self.name, True, GREEN_COLOR), position)
