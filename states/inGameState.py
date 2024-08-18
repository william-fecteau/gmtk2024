import os

import numpy as np
import pygame
import sympy.core.numbers as spnumbers
from sympy import false, true

from constants import (BLACK, DARK_GRAY, GREEN_COLOR, LIGHTER_GRAY,
                       SCREEN_SIZE, WORLD_COLOR)
from cutscenes.cutsceneManager import CutsceneManager
from levels import Card, evaluate_solution, load_level
from sand_simulathor.sand_simulator import SandSimulator
from states.payloads import InGameStatePayload
from utils import get_max_levels_per_world, get_max_worlds, resource_path

from .state import State


class HelpUi:
    def __init__(self, help_text: str):
        width, height = SCREEN_SIZE
        width *= 0.8
        height *= 0.2
        self.surf = pygame.Surface((width, height))
        self.surf.fill(LIGHTER_GRAY)
        self.surf.set_alpha(253)

        font_smoll = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'), 24)

        self.is_open = False
        display = pygame.display.get_surface().get_rect()
        self.help_surf_rect = self.surf.get_rect(bottom=display.bottom, centerx=display.centerx)
        self.help_surf_rect.move_ip(0, -30)

        textLines = help_text.split("\n")

        for i in range(0, len(textLines)):
            textSurface : pygame.Surface = font_smoll.render(textLines[i], True, BLACK)
            textPosition = textSurface.get_rect(center = self.surf.get_rect().center).move(0, (i - 1) * 25)
            self.surf.blit(textSurface, textPosition)

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
        self.cardUI: CardUi | None = None

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
        self.isHover = False
        # self.surf.fill((147, 147, 147))
        self.cardImage = pygame.image.load(resource_path('./res/carteV2.png')).convert_alpha()
        self.cardImageHover = pygame.image.load(resource_path('./res/carteV1.png')).convert_alpha()
        self.surf.blit(self.cardImage, pygame.Rect(0, 0, 80, 80))

        self.card_text = self.get_card_display()

        self.lenght = 48
        if self.card_text.__len__() > 3:
            self.lenght = 24
        if self.card_text.__len__() > 5:
            self.lenght = 18

        text_surf = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                     self.lenght).render(self.card_text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.surf.get_rect().center)
        self.surf.blit(text_surf, text_rect)

        self.rect = pygame.Rect(x, y, size, size)
        self.initPos = self.rect.topleft
        self.needUpdate = False

    def get_card_display(self) -> str:
        value = self.card.value

        if value == "*":
            return "x"
        elif value == "/":
            return "÷"
        elif value == "sqrt":
            return "√"
        elif value.startswith("sqrt("):
            return value.replace("sqrt(", "√").replace(")", "")
        elif value == "pi":
            return "π"

        return value

    def move(self, pos: tuple[int, int]):
        self.rect.topleft = pos

    def draw(self, surface: pygame.Surface):
        if (self.isHover):
            self.surf.blit(self.cardImageHover, pygame.Rect(0, 0, 80, 80))
        else:
            self.surf.blit(self.cardImage, pygame.Rect(0, 0, 80, 80))
        self.card_text = self.get_card_display()
        text_surf = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                     self.lenght).render(self.card_text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.surf.get_rect().center)
        self.surf.blit(text_surf, text_rect)

        surface.blit(self.surf, self.rect.topleft)

    def setComebackPosition(self):
        self.needUpdate = True

    def moveToInitPost(self):
        distance = 10
        distanceX = abs(self.rect.topleft[0] - self.initPos[0])
        distanceY = abs(self.rect.topleft[1] - self.initPos[1])

        if (distanceX == 0):
            ratioDistanceY = distanceY/1
            parcoursY = distance*ratioDistanceY
        else:
            ratioDistanceY = distanceY/distanceX
            parcoursY = distance*ratioDistanceY
        if (distanceY == 0):
            ratioDistanceX = distanceX/1
            parcoursX = distance*ratioDistanceX
        else:
            ratioDistanceX = distanceX/distanceY
            parcoursX = distance*ratioDistanceX

        newX = self.rect.topleft[0]
        newY = self.rect.topleft[1]
        if (abs(self.rect.topleft[0] - self.initPos[0]) < parcoursX):
            if (self.rect.topleft[0] > self.initPos[0]):
                newX = self.rect.topleft[0] - (self.rect.topleft[0] - self.initPos[0])
            if (self.rect.topleft[0] < self.initPos[0]):
                newX = self.rect.topleft[0] + (self.rect.topleft[0] - self.initPos[0])

        if (abs(self.rect.topleft[1] - self.initPos[1]) < parcoursY):
            if (self.rect.topleft[1] > self.initPos[1]):
                newY = self.rect.topleft[1] - (self.rect.topleft[1] - self.initPos[1])
            if (self.rect.topleft[1] < self.initPos[1]):
                newY = self.rect.topleft[1] + (self.rect.topleft[1] - self.initPos[1])

        if (newX > self.initPos[0]):
            newX = self.rect.topleft[0] - parcoursX
        if (newY > self.initPos[1]):
            newY = self.rect.topright[1] - parcoursY
        if (newX < self.initPos[0]):
            newX = self.rect.topleft[0] + parcoursX
        if (newY < self.initPos[1]):
            newY = self.rect.topleft[1] + parcoursY
        try:
            self.rect.topleft = (int(newX), int(newY))
        except:
            self.rect.topleft = self.initPos

        if (self.rect.topleft == self.initPos):
            self.needUpdate = False


class SandUi:
    def __init__(self, currentWorld: int):
        color = 0,0,0
        colorStr = "WORLD_" + str(currentWorld) + "_COLOR"
        try:
            color = WORLD_COLOR.get(colorStr)
        except:
            color = 0,0,0

        self.sim = SandSimulator(color)

    def update(self):
        self.sim.update_particles()

    def draw(self, overflow_ammount, surface):
        self.sim.draw_particles(overflow_ammount, surface)


class InGameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.background = pygame.image.load(resource_path('./res/MenuImg/LevelBackground.png')).convert_alpha()
        self.card_drop = pygame.mixer.Sound(resource_path('./res/Sfx_Card_Drop.mp3'))
        self.card_pickup = pygame.mixer.Sound(resource_path('./res/Sfx_Card_Pickup.mp3'))
        self.level_clear = pygame.mixer.Sound(resource_path('./res/Sfx_Level_clear.mp3'))
        self.cutsceneManager = CutsceneManager()

    # ==============================================================================================================
    # Update
    # ==============================================================================================================
    def update(self) -> None:
        # Event handling
        self.last_mouse_move = pygame.mouse.get_rel()
        for event in self.game.events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down()
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up()

        # Card dragging
        mouse_pos = pygame.mouse.get_pos()
        if self.selected_card is not None:
            offset_pos = np.array(mouse_pos) - np.array(self.mouse_click_offset)
            self.selected_card.move(offset_pos)  # type: ignore
        elif self.selected_card is None:
            self.is_over_card(mouse_pos)
        # Card snap to initial position
        for card in self.cards_ui:
            if card.needUpdate == True:
                card.moveToInitPost()

        # If overflow, switch to next level
        if self.current_answer is not None and self.current_answer > (2 ** self.level.nb_bits_to_overflow) - 1:
            self.level_completed()

    def is_over_card(self, mouse_pos: tuple[int, int]):
        for card_ui in self.cards_ui:
            if card_ui.rect.collidepoint(mouse_pos):
                card_ui.isHover = True
            else:
                card_ui.isHover = False

    def handle_mouse_down(self):
        mouse_pos = pygame.mouse.get_pos()

        # Card selection
        if self.selected_card is None:
            for card_ui in self.cards_ui:
                if card_ui.rect.collidepoint(mouse_pos):
                    self.selected_card = card_ui
                    pygame.mixer.Sound.play(self.card_pickup)
                    # self.selected_card.saveInitialPos(card_ui.rect.topleft)
                    self.mouse_click_offset = np.array(mouse_pos) - np.array(card_ui.rect.topleft)
                    break

        # Help UI
        if self.help_btn_rect.collidepoint(mouse_pos):
            if self.help_ui.is_open:
                self.help_ui.close()
            else:
                self.help_ui.open()
        elif self.help_ui.is_open and not self.help_ui.help_surf_rect.collidepoint(mouse_pos):
            self.help_ui.close()

        # Next Button
        if self.completed:
            if self.next_button_rect.collidepoint(mouse_pos):
                self.go_next_level()

    def handle_mouse_up(self):
        if self.selected_card != None:
            pygame.mixer.Sound.play(self.card_drop)
            self.dontMove = False
            for slot in self.card_slots:
                if slot.cardInside(self.selected_card):
                    self.dontMove = True
                    if slot.card != None and slot.cardUI != None and slot.cardUI != self.selected_card:
                        slot.cardUI.setComebackPosition()
                        self.selected_card.rect.center = slot.rect.center
                        slot.card = self.selected_card.card
                        slot.cardUI = self.selected_card
                    if slot.card == None and slot.cardUI == None:
                        self.selected_card.rect.center = slot.rect.center

                        slot.card = self.selected_card.card
                        slot.cardUI = self.selected_card

            if self.dontMove == False:
                self.selected_card.setComebackPosition()
            self.selected_card = None
        for slot in self.card_slots:
            for card_ui in self.cards_ui:
                if slot.cardInside(card_ui):
                    slot.setColor(GREEN_COLOR)
                    if slot.card == None and slot.cardUI == None:
                        card_ui.rect.center = slot.rect.center

                        slot.card = card_ui.card
                        slot.cardUI = card_ui
                    break
                else:
                    slot.setColor(DARK_GRAY)
                    slot.card = None
                    slot.cardUI = None

        self.current_answer = self.getAnswer()

    def level_completed(self) -> None:
        if (not self.completed):
            pygame.mixer.Sound.play(self.level_clear)

        self.completed = true

    def go_next_level(self) -> None:
        max_worlds = get_max_worlds()
        max_levels = get_max_levels_per_world(self.current_world)

        next_world = self.current_world
        next_level = self.current_level + 1

        if next_level > max_levels:
            next_world += 1
            next_level = 1

        if next_world >= max_worlds:
            self.game.switchState("CreditsState")

        self.game.switchState("InGameState", InGameStatePayload(next_world, next_level))

    def getAnswer(self) -> float | None:
        solutions: list[Card] = []
        for slot in self.card_slots:
            if slot.card is not None:
                solutions.append(slot.card)

        try:
            value = evaluate_solution(self.level, solutions)  # type: ignore
        except Exception as e:
            return None

        return value

    # ==============================================================================================================
    # Drawing
    # ==============================================================================================================
    def draw(self, screen) -> None:
        self.cutsceneManager.DisplayCustcene(screen)

        screen.blit(self.background, pygame.Rect(0, 0, 1280, 720))

        if (self.current_answer is not None):
            overflow_ammount = self.current_answer * 100 / (2 ** self.level.nb_bits_to_overflow)
        else:
            overflow_ammount = 0.0
        self.sand_ui.draw(overflow_ammount, screen)

        self.sand_ui.update()
        for card_slot in self.card_slots:
            card_slot.draw(screen)

        for card in self.cards_ui:
            card.draw(screen)

        self.draw_total(screen)

        if self.completed:
            self.draw_next(screen)

        self.draw_help_ui(screen)

    def draw_total(self, screen: pygame.Surface) -> None:
        # Choosing color
        color_gradient = [
            (255, 255, 255),
            (255, 211, 218),
            (212, 149, 149),
            (210, 127, 127),
            (202, 107, 107),
            (200, 92, 92),
            (204, 63, 63),
            (211, 0, 0),
            (186, 8, 40),
            (153, 0, 0),
        ]

        value = self.current_answer if self.current_answer is not None else 0

        color_index = int(value * len(color_gradient) / (2 ** self.level.nb_bits_to_overflow - 1))
        color_index = np.clip(color_index, 0, len(color_gradient) - 1)  # Just to be sure so it doesnt boom
        color = color_gradient[color_index]

        # Parsing answer to text
        parsed_answer = "???"
        if self.current_answer is not None:
            if isinstance(self.current_answer, spnumbers.Integer):
                parsed_answer = f'{self.current_answer}'
            else:
                parsed_answer = f'{self.current_answer:.2f}'

        # Drawing total
        self.total_text = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                           80).render(parsed_answer, True, color)
        self.total_rect = self.total_text.get_rect(center=self.game.screen.get_rect().center)
        self.total_rect.y = int(SCREEN_SIZE[1] / 6)

        # Drawing binary representation
        binary_str = "0"
        if value >= 0:
            binary_str = bin(int(value))[2:]

        # If overflow, we actually overflow
        if value > 2 ** self.level.nb_bits_to_overflow - 1:
            binary_str = "1"

        binary_str = binary_str.zfill(self.level.nb_bits_to_overflow)

        self.desc_goal = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                          40).render(binary_str, True, color)
        self.desc_rect = self.desc_goal.get_rect(center=self.total_rect.center)
        self.desc_rect.move_ip(0, 50)

        # Blitting everything
        screen.blit(self.desc_goal, self.desc_rect)
        screen.blit(self.total_text, self.total_rect)
        screen.blit(self.goal_text, self.goal_rect)
        screen.blit(self.world_text, self.world_rect)

    def draw_help_ui(self, screen: pygame.Surface) -> None:
        help_surface = pygame.font.Font(resource_path(
            './res/TTOctosquaresTrialRegular.ttf'), 48).render("?", True, (255, 255, 255))
        posHelpButtion = (screen.get_rect().bottomleft[0]+30, screen.get_rect().bottomleft[1]-20)
        self.help_btn_rect = help_surface.get_rect(bottomleft=posHelpButtion)
        screen.blit(help_surface, self.help_btn_rect)

        self.help_ui.draw(screen)

    def draw_next(self, screen: pygame.Surface) -> None:

        surf = pygame.Surface((150, 80))
        buttonImage = pygame.image.load(resource_path('./res/carteV2.png')).convert_alpha()
        # surf.blit(buttonImage, pygame.Rect(0, 0, 150, 80))
        surf.fill((147, 147, 147))

        next_button_text = pygame.font.Font(resource_path(
            './res/TTOctosquaresTrialRegular.ttf'), 48).render("Next", True, (0, 0, 0))
        text_rect = next_button_text.get_rect(center=surf.get_rect().center)
        surf.blit(next_button_text, text_rect)
        screen.blit(surf, self.next_button_rect)

    # ==============================================================================================================
    # State management
    # ==============================================================================================================

    def onEnterState(self, payload: InGameStatePayload) -> None:
        pathStr = f"res/worlds/{payload.world}/{payload.level}.json"
        pathLevel = os.path.join(pathStr)

        self.current_world = payload.world
        self.current_level = payload.level
        self.level = load_level(pathLevel)

        self.current_answer: float | None = None
        self.selected_card: CardUi | None = None
        self.mouse_click_offset = (0, 0)

        self.init_card_slots()

        if (self.cutsceneManager.queuedCutscene != payload.world):
            self.cutsceneManager.QueueCutscene(payload.world)

        self.help_ui = HelpUi(self.level.hint)
        self.sand_ui = SandUi(self.current_world)

    def onExitState(self) -> None:
        pass

    def init_card_slots(self):
        self.card_slots: list[CardSlotUi] = []
        self.cards_ui: list[CardUi] = []

        self.goal_text = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                          128).render(f'{(2 ** self.level.nb_bits_to_overflow) - 1:,}', True, (255, 255, 255))
        self.goal_rect = self.goal_text.get_rect(center=self.game.screen.get_rect().center)
        self.goal_rect.y = -20  # 1/18 * self.game.screen.get_rect().h

        self.world_text = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                           32).render('World ' + str(self.current_world) + ' Level ' + str(self.current_level), True, (255, 255, 255))
        self.world_rect = self.world_text.get_rect(bottomright=self.game.screen.get_rect().bottomright)
        self.world_rect.x -= 15
        self.world_rect.y -= 10

        self.next_button_rect = pygame.Rect(self.game.screen.get_rect().right - 200,
                                            self.game.screen.get_rect().bottom - 150, 150, 80)
        self.completed = false

        slot_size = 100
        slot_offset = 20

        card_size = 80
        card_offset = 20

        nb_cards = len(self.level.cards)

        slot_width = nb_cards * (slot_size + slot_offset)
        card_width = nb_cards * (card_size + card_offset)

        nb_separator = 0
        if slot_width > 1280:
            nb_separator = 1280 // (slot_size + slot_offset)
            slot_width = nb_separator * (slot_size + slot_offset)
            card_width = nb_separator * (card_size + card_offset)

        start_slot = np.array(self.game.screen.get_rect().center) - np.array((slot_width // 2, slot_size // 2))
        start_slot[1] = start_slot[1] - 25
        start_card = np.array(self.game.screen.get_rect().center) - \
            np.array((card_width // 2, -card_size // 2 - 20))

        resetCount = 0
        for i, card in enumerate(self.level.cards):
            self.card_slots.append(CardSlotUi(
                start_slot[0] + (i - nb_separator * resetCount) * (slot_size + slot_offset), start_slot[1] + ((slot_offset + slot_size) * resetCount), slot_size))
            if nb_separator and np.mod(i, nb_separator) == nb_separator - 1:
                resetCount += 1

        resetCount = 0
        for i, card in enumerate(self.level.cards):
            self.cards_ui.append(
                CardUi(card, start_card[0] + (i - nb_separator * resetCount) * (card_size + card_offset), ((card_offset + card_size) * resetCount) + self.card_slots[-1].rect.bottom + 20, card_size))
            if nb_separator and np.mod(i, nb_separator) == nb_separator - 1:
                resetCount += 1
