import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def customDraw(self, screen: pygame.Surface, cameraOffset: pygame.math.Vector2) -> None:
        for sprite in self.sprites():
            offsetPos = (sprite.rect.x, sprite.rect.y) - cameraOffset
            screen.blit(sprite.image, offsetPos)
