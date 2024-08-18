
import os

import numpy as np
import pygame
import sympy.core.numbers as spnumbers

from constants import DARK_GRAY, GREEN_COLOR
from levels import Card, evaluate_solution, load_level
from states.payloads import InGameStatePayload
from utils import resource_path

from .state import State


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
        text_surf = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                     48).render(card.value, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.surf.get_rect().center)
        self.surf.blit(text_surf, text_rect)

        self.rect = pygame.Rect(x, y, size, size)

        self.needUpdate = False

    def move(self, pos: tuple[int, int]):
        self.rect.topleft = pos

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect.topleft)
    
    def saveInitialPos(self, pos: tuple[int, int]) ->None:
        self.initPos = pos
    
    def setComebackPosition(self, pos: tuple[int, int]):
        self.needUpdate = True
        print(self.rect.topleft[0])

        distance = 10
        distanceX = abs(self.rect.topleft[0] - self.initPos[0])
        distanceY = abs(self.rect.topleft[1] - self.initPos[1])
        
    #I'm sorry
    def moveToInitPost(self):
        distance = 10
        distanceX = abs(self.rect.topleft[0] - self.initPos[0])
        distanceY = abs(self.rect.topleft[1] - self.initPos[1])

        if(distanceX == 0):
            ratioDistanceY = distanceY/1
            parcoursY = distance*ratioDistanceY
        else:
            ratioDistanceY = distanceY/distanceX
            parcoursY = distance*ratioDistanceY
        if(distanceY == 0):
            ratioDistanceX = distanceX/1
            parcoursX = distance*ratioDistanceX
        else:
            ratioDistanceX = distanceX/distanceY
            parcoursX = distance*ratioDistanceX

        newX = self.rect.topleft[0]
        newY = self.rect.topleft[1]
        if(abs(self.rect.topleft[0] - self.initPos[0]) < parcoursX):
            if(self.rect.topleft[0] > self.initPos[0]):
                newX = self.rect.topleft[0] - (self.rect.topleft[0] - self.initPos[0])
            if(self.rect.topleft[0] < self.initPos[0]):
                newX = self.rect.topleft[0] + (self.rect.topleft[0] - self.initPos[0])

        if(abs(self.rect.topleft[1] - self.initPos[1]) < parcoursY):
            if(self.rect.topleft[1] > self.initPos[1]):
                newY = self.rect.topleft[1] - (self.rect.topleft[1] - self.initPos[1])
            if(self.rect.topleft[1] < self.initPos[1]):
                newY = self.rect.topleft[1] + (self.rect.topleft[1] - self.initPos[1])

        
        if(newX > self.initPos[0]):
            newX = self.rect.topleft[0] - parcoursX
        if(newY > self.initPos[1]):
            newY = self.rect.topright[1] - parcoursY
        if(newX < self.initPos[0]):
            newX = self.rect.topleft[0] + parcoursX
        if(newY < self.initPos[1]):
            newY = self.rect.topleft[1] + parcoursY

        self.rect.topleft = (int(newX), int(newY))

        if(self.rect.topleft == self.initPos):
            self.needUpdate = False
        


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
                for card_ui in self.cards_ui:
                    if card_ui.rect.collidepoint(mouse_pos):
                        self.selected_card = card_ui
                        self.selected_card.saveInitialPos(card_ui.rect.topleft)
                        self.mouse_click_offset = np.array(mouse_pos) - np.array(card_ui.rect.topleft)
                        break
        else:
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

        for card in self.cards_ui:
            if card.needUpdate == True:
                card.moveToInitPost()

    def draw(self, screen) -> None:
        for card_slot in self.card_slots:
            card_slot.draw(screen)

        for card in self.cards_ui:
            card.draw(screen)

        screen.blit(self.goal_text, self.goal_rect)
        screen.blit(self.desc_goal, self.desc_rect)

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

    def onExitState(self) -> None:
        pass
