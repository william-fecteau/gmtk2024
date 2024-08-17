
import numpy as np
import pygame

from levels import load_level
from states.payloads import InGameStatePayload

from .state import State


class CharacterSlot:
    def __init__(self, x: int, y: int, size: int):
        self.surf = pygame.Surface((size, size))
        self.surf.fill((46, 46, 46))

        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect.topleft)


class Character:
    def __init__(self, character: str, x: int, y: int, size: int):
        self.character = character

        self.surf = pygame.Surface((size, size))
        self.surf.fill((147, 147, 147))

        text_surf = pygame.font.Font(None, 32).render(character, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.surf.get_rect().center)
        self.surf.blit(text_surf, text_rect)

        self.rect = pygame.Rect(x, y, size, size)

    def move(self, pos: tuple[int, int]):
        self.rect.topleft = pos

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect.topleft)


class InGameState(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self) -> None:
        for event in self.game.events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")

        self.last_mouse_move = pygame.mouse.get_rel()

        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.selected_character is None:
                for character in self.characters:
                    if character.rect.collidepoint(mouse_pos):
                        self.selected_character = character
                        self.mouse_click_offset = np.array(mouse_pos) - np.array(character.rect.topleft)
                        break
        else:
            self.selected_character = None

        if self.selected_character is not None:
            offset_pos = np.array(mouse_pos) - np.array(self.mouse_click_offset)
            self.selected_character.move(offset_pos)  # type: ignore

    def draw(self, screen) -> None:
        for character_slot in self.character_slots:
            character_slot.draw(screen)

        for character in self.characters:
            character.draw(screen)

    def init_character_slots(self):
        self.character_slots: list[CharacterSlot] = []
        self.characters: list[Character] = []

        slot_size = 60
        slot_offset = 10

        character_size = 40
        character_offset = 10

        nb_characters = len(self.level.cards)

        slot_width = nb_characters * (slot_size + slot_offset)
        character_width = nb_characters * (character_size + character_offset)

        start_slot = np.array(self.game.screen.get_rect().center) - np.array((slot_width // 2, slot_size // 2))
        start_character = np.array(self.game.screen.get_rect().center) - \
            np.array((character_width // 2, -character_size // 2 - 20))

        for i, card in enumerate(self.level.cards):
            value = card.value

            self.character_slots.append(CharacterSlot(
                start_slot[0] + i * (slot_size + slot_offset), start_slot[1], slot_size))
            self.characters.append(
                Character(value, start_character[0] + i * (character_size + character_offset), start_character[1], character_size))

    def onEnterState(self, payload: InGameStatePayload) -> None:
        self.level = load_level("res/levels/1.json")

        self.selected_character: Character | None = None
        self.mouse_click_offset = (0, 0)
        self.init_character_slots()

    def onExitState(self) -> None:
        pass
