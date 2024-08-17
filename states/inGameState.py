
import os

import numpy as np
import pygame

from constants import DARK_GRAY, GREEN_COLOR
from levels import load_level
from states.payloads import InGameStatePayload

from .state import State


class CardSlot:
    def __init__(self, x: int, y: int, size: int):
        self.surf = pygame.Surface((size, size))
        self.surf.fill((46, 46, 46))

        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect.topleft)

    def setColor(self, color):
        self.surf.fill(color)

    def cardInside(self, card):
        if self.rect.contains(card.rect):
            return True
        return False


class Card:
    def __init__(self, card: str, x: int, y: int, size: int):
        self.card = card

        self.surf = pygame.Surface((size, size))
        self.surf.fill((147, 147, 147))

        text_surf = pygame.font.Font(None, 32).render(card, True, (0, 0, 0))
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
            if self.selected_card is None:
                for card in self.cards:
                    if card.rect.collidepoint(mouse_pos):
                        self.selected_card = card
                        self.mouse_click_offset = np.array(mouse_pos) - np.array(card.rect.topleft)
                        break
        else:
            self.selected_card = None
            for slot in self.card_slots:
                for card in self.cards:
                    if slot.cardInside(card):
                        slot.setColor(GREEN_COLOR)
                        break
                    else:
                        slot.setColor(DARK_GRAY)

        if self.selected_card is not None:
            offset_pos = np.array(mouse_pos) - np.array(self.mouse_click_offset)
            self.selected_card.move(offset_pos)  # type: ignore

    def draw(self, screen) -> None:
        for card_slot in self.card_slots:
            card_slot.draw(screen)

        for card in self.cards:
            card.draw(screen)

    def init_card_slots(self):
        self.card_slots: list[CardSlot] = []
        self.cards: list[Card] = []

        slot_size = 60
        slot_offset = 10

        card_size = 40
        card_offset = 10

        nb_cards = len(self.level.cards)

        slot_width = nb_cards * (slot_size + slot_offset)
        card_width = nb_cards * (card_size + card_offset)

        start_slot = np.array(self.game.screen.get_rect().center) - np.array((slot_width // 2, slot_size // 2))
        start_card = np.array(self.game.screen.get_rect().center) - \
            np.array((card_width // 2, -card_size // 2 - 20))

        for i, card in enumerate(self.level.cards):
            value = card.value

            self.card_slots.append(CardSlot(
                start_slot[0] + i * (slot_size + slot_offset), start_slot[1], slot_size))
            self.cards.append(
                Card(value, start_card[0] + i * (card_size + card_offset), start_card[1], card_size))

    def onEnterState(self, payload: InGameStatePayload) -> None:
        pathLevel = os.path.join(f"res/worlds/{payload.world}/{payload.level}.json")
        self.level = load_level(pathLevel)

        self.selected_card: Card | None = None
        self.mouse_click_offset = (0, 0)
        self.init_card_slots()

    def onExitState(self) -> None:
        pass
