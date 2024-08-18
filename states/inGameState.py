
import os

import numpy as np
import pygame
import sympy.core.numbers as spnumbers

from constants import DARK_GRAY, GREEN_COLOR, LIGHT_GRAY, SCREEN_SIZE
from levels import Card, evaluate_solution, load_level
from states.payloads import InGameStatePayload
from utils import resource_path

from .state import State


class HelpUi:
    def __init__(self, cards: list[Card]):
        width, height = SCREEN_SIZE
        width *= 0.8
        height *= 0.8
        self.surf = pygame.Surface((width, height))
        self.surf.fill(LIGHT_GRAY)
        self.surf.set_alpha(253)

        font = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'), 48)

        close_surf = font.render("X", True, (0, 0, 0))
        self.close_rect = close_surf.get_rect(topleft=(width - 50, 10))
        self.surf.blit(close_surf, self.close_rect)

        self.is_open = False
        self.help_surf_rect = self.surf.get_rect(center=pygame.display.get_surface().get_rect().center)

        self.close_rect.move_ip(self.help_surf_rect.topleft)

    def draw(self, screen: pygame.Surface):
        if self.is_open:
            screen.blit(self.surf, self.help_surf_rect)

    def close(self):
        self.is_open = False

    def open(self):
        self.is_open = True


class CardSlotUi:
    def __init__(self, x: int, y: int, size: int):
        self.surf = pygame.Surface((size, size))
        self.surf.fill(DARK_GRAY)
        self.card: Card | None = None

        self.rect = pygame.Rect(x, y, size, size)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect.topleft)

    def setColor(self, color: tuple) -> None:
        self.surf.fill(color)

    def cardInside(self, card) -> bool:
        largeRect = self.rect.inflate(50, 50)
        return largeRect.contains(card.rect)


class CardUi:
    def __init__(self, card: Card, x: int, y: int, size: int):
        self.card = card

        self.surf = pygame.Surface((size, size))
        self.surf.fill((147, 147, 147))

        card_text = self.get_card_display()
        text_surf = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                     48).render(card_text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.surf.get_rect().center)
        self.surf.blit(text_surf, text_rect)

        self.rect = pygame.Rect(x, y, size, size)
        self.needUpdate = False

    def get_card_display(self) -> str:
        value = self.card.value

        if value == "*":
            return "x"
        elif value == "/":
            return "÷"
        elif value == "sqrt":
            return "√"
        elif value == "sqrt(":
            return "√("
        elif value == "pi":
            return "π"

        return value

    def move(self, pos: tuple[int, int]):
        self.rect.topleft = pos

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect.topleft)

    def saveInitialPos(self, pos: tuple[int, int]) -> None:
        self.initPos = pos

    def setComebackPosition(self, pos: tuple[int, int]):
        self.needUpdate = True

    def moveToInitPost(self):
        newX = self.rect.topleft[0]
        newY = self.rect.topleft[1]
        if (abs(self.rect.topleft[0] - self.initPos[0]) < 10):
            if (self.rect.topleft[0] > self.initPos[0]):
                newX = self.rect.topleft[0] - (self.rect.topleft[0] - self.initPos[0])
            if (self.rect.topleft[0] < self.initPos[0]):
                newX = self.rect.topleft[0] + (self.rect.topleft[0] - self.initPos[0])

        if (abs(self.rect.topleft[1] - self.initPos[1]) < 10):
            if (self.rect.topleft[1] > self.initPos[1]):
                newY = self.rect.topleft[1] - (self.rect.topleft[1] - self.initPos[1])
            if (self.rect.topleft[1] < self.initPos[1]):
                newY = self.rect.topleft[1] + (self.rect.topleft[1] - self.initPos[1])

        if (newX > self.initPos[0]):
            newX = self.rect.topleft[0] - 10
        if (newY > self.initPos[1]):
            newY = self.rect.topright[1] - 10
        if (newX < self.initPos[0]):
            newX = self.rect.topleft[0] + 10
        if (newY < self.initPos[1]):
            newY = self.rect.topleft[1] + 10
        self.rect.topleft = (newX, newY)

        if (self.rect.topleft == self.initPos):
            self.needUpdate = False


class InGameState(State):

    def __init__(self, game):
        super().__init__(game)

    def update(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        self.last_mouse_move = pygame.mouse.get_rel()
        for event in self.game.events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Card selection
                if self.selected_card is None:
                    for card_ui in self.cards_ui:
                        if card_ui.rect.collidepoint(mouse_pos):
                            self.selected_card = card_ui
                            self.selected_card.saveInitialPos(card_ui.rect.topleft)
                            self.mouse_click_offset = np.array(mouse_pos) - np.array(card_ui.rect.topleft)
                            break

                # Help UI
                if self.help_btn_rect.collidepoint(mouse_pos):
                    if self.help_ui.is_open:
                        self.help_ui.close()
                    else:
                        self.help_ui.open()

                if self.help_ui.close_rect.collidepoint(mouse_pos):
                    self.help_ui.close()

            if event.type == pygame.MOUSEBUTTONUP:
                if self.selected_card != None:
                    self.dontMove = False
                    for slot in self.card_slots:
                        if slot.cardInside(self.selected_card):
                            self.dontMove = True

                    if self.dontMove == False:
                        self.selected_card.setComebackPosition(self.selected_card.initPos)
                    self.selected_card = None
                for slot in self.card_slots:
                    for card_ui in self.cards_ui:
                        if slot.cardInside(card_ui):
                            slot.setColor(GREEN_COLOR)
                            slot.card = card_ui.card
                            break
                        else:
                            slot.setColor(DARK_GRAY)
                            slot.card = None
                self.current_answer = self.getAnswer()

        if self.selected_card is not None:
            offset_pos = np.array(mouse_pos) - np.array(self.mouse_click_offset)
            self.selected_card.move(offset_pos)  # type: ignore

    def draw_total(self, screen: pygame.Surface) -> None:
        parsed_answer = "???"
        if self.current_answer is not None:
            if isinstance(self.current_answer, spnumbers.Integer):
                parsed_answer = f'{self.current_answer:,}'
            else:
                parsed_answer = f'{self.current_answer:.2f}'

        self.total_text = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                           80).render(parsed_answer, True, (255, 255, 255))
        self.total_rect = self.total_text.get_rect(center=self.game.screen.get_rect().center)
        self.total_rect.y = self.totalHeight
        screen.blit(self.total_text, self.total_rect)

        screen.blit(self.goal_text, self.goal_rect)
        screen.blit(self.desc_goal, self.desc_rect)

    def draw_help_ui(self, screen: pygame.Surface) -> None:
        help_surface = pygame.font.Font(resource_path(
            './res/TTOctosquaresTrialRegular.ttf'), 48).render("?", True, (255, 255, 255))
        self.help_btn_rect = help_surface.get_rect(bottomleft=screen.get_rect().bottomleft)
        screen.blit(help_surface, self.help_btn_rect)

        self.help_ui.draw(screen)

    def draw(self, screen) -> None:
        for card_slot in self.card_slots:
            card_slot.draw(screen)

        for card in self.cards_ui:
            card.draw(screen)

        self.draw_total(screen)

        self.draw_help_ui(screen)

    def init_card_slots(self):
        self.card_slots: list[CardSlotUi] = []
        self.cards_ui: list[CardUi] = []

        self.goal_text = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                          128).render(f'{(2 ** self.level.nb_bits_to_overflow) - 1:,}', True, (255, 255, 255))
        self.goal_rect = self.goal_text.get_rect(center=self.game.screen.get_rect().center)
        self.goal_rect.y = 1/15 * self.game.screen.get_rect().h

        self.desc_goal = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                          64).render(str(self.level.nb_bits_to_overflow) + '-bit Integer', True, (255, 255, 255))
        self.desc_rect = self.desc_goal.get_rect(center=self.game.screen.get_rect().center)
        self.desc_rect.y = 1/4 * self.game.screen.get_rect().h

        slot_size = 100
        slot_offset = 20

        card_size = 80
        card_offset = 20

        nb_cards = len(self.level.cards)

        slot_width = nb_cards * (slot_size + slot_offset)
        card_width = nb_cards * (card_size + card_offset)

        start_slot = np.array(self.game.screen.get_rect().center) - np.array((slot_width // 2, slot_size // 2))
        start_card = np.array(self.game.screen.get_rect().center) - \
            np.array((card_width // 2, -card_size // 2 - 20))

        for i, card in enumerate(self.level.cards):
            self.card_slots.append(CardSlotUi(
                start_slot[0] + i * (slot_size + slot_offset), start_slot[1], slot_size))
            self.cards_ui.append(
                CardUi(card, start_card[0] + i * (card_size + card_offset), start_card[1], card_size))

        self.totalHeight = self.card_slots[-1].rect.bottom

    def getAnswer(self) -> float | None:
        solutions: list[Card] = []
        for slot in self.card_slots:
            if slot.card is not None:
                solutions.append(slot.card)

        try:
            value = evaluate_solution(self.level, solutions)  # type: ignore
        except:
            return None

        return value

    def onEnterState(self, payload: InGameStatePayload) -> None:
        pathStr = f"res/worlds/{payload.world}/{payload.level}.json"
        pathLevel = os.path.join(pathStr)
        self.level = load_level(pathLevel)

        self.current_answer: float | None = None
        self.selected_card: CardUi | None = None
        self.mouse_click_offset = (0, 0)

        self.init_card_slots()

        self.help_ui = HelpUi(self.level.cards)

    def onExitState(self) -> None:
        pass
