
import numpy as np
import pygame
import sympy.core.numbers as spnumbers
from sympy import false, true

from constants import BLACK, DARK_GRAY, GREEN_COLOR, SCREEN_SIZE, WORLD_COLORS
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
        self.surf = pygame.Surface((width, height), pygame.SRCALPHA)
        self.boxImage = pygame.image.load(resource_path('./res/HintTextbox.png')).convert_alpha()
        self.surf.blit(self.boxImage, pygame.Rect(0, 0, 80, 80))

        font_smoll = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'), 24)

        self.is_open = False
        display = pygame.display.get_surface().get_rect()
        self.help_surf_rect = self.surf.get_rect(bottom=display.bottom, centerx=display.centerx)
        self.help_surf_rect.move_ip(0, -30)

        textLines = help_text.split("\n")

        for i in range(0, len(textLines)):
            textSurface: pygame.Surface = font_smoll.render(textLines[i], True, BLACK)
            textPosition = textSurface.get_rect(center=self.surf.get_rect().center).move(0, (i - 1) * 25)
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
        largeRect = self.rect.inflate(100, 100)
        return largeRect.contains(card.rect)


class CardUi:
    def __init__(self, card: Card, x: int, y: int, size: int):
        self.card = card

        self.surf = pygame.Surface((size, size), pygame.SRCALPHA)
        self.isHover = False
        # self.surf.fill((147, 147, 147))
        self.cardImage = pygame.image.load(resource_path('./res/carteV2.png')).convert_alpha()
        self.cardImageHover = pygame.image.load(resource_path('./res/carteV1.png')).convert_alpha()
        self.surf.blit(self.cardImage, pygame.Rect(0, 0, 80, 80))

        self.card_text = self.get_card_display()

        self.lenght = 48
        if self.card_text.__len__() >= 3:
            self.lenght = 22
        if self.card_text.__len__() >= 5:
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
        color = WORLD_COLORS.get(currentWorld, BLACK)
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
        self.next_world_sfx = pygame.mixer.Sound(resource_path('./res/NextWorldSFX.mp3'))
        self.cutsceneManager = CutsceneManager()
        self.sandEnabled = True

    # ==============================================================================================================
    # Update
    # ==============================================================================================================

    def update(self) -> None:
        # Event handling
        self.last_mouse_move = pygame.mouse.get_rel()
        for event in self.game.events:
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                self.game.switchState("MenuState")
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                self.resetCards()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down()
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up()
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.sandEnabled = not self.sandEnabled

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

        if self.tutorial_ui is not None:
            self.tutorial_ui.on_click(mouse_pos)

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
            pygame.mixer.Sound.play(self.next_world_sfx)

        if next_world >= max_worlds:
            self.game.switchState("CreditsState")

        self.game.switchState("InGameState", InGameStatePayload(next_world, next_level))

    def getAnswer(self) -> float | None:
        solutions: list[Card] = []
        for slot in self.card_slots:
            if slot.card is not None:
                solutions.append(slot.card)

        try:
            value = evaluate_solution(self.level, solutions, self.current_world, self.game)  # type: ignore
        except Exception as e:
            return None

        return value

    def resetCards(self) -> None:
        for slot in self.card_slots:
            if slot.card is not None and slot.cardUI is not None:
                slot.setColor(DARK_GRAY)
                slot.cardUI.setComebackPosition()
                slot.card = None
                slot.cardUI = None

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

        if (self.sandEnabled):
            self.sand_ui.update()
            self.sand_ui.draw(overflow_ammount, screen)

        for card_slot in self.card_slots:
            card_slot.draw(screen)

        for card in self.cards_ui:
            card.draw(screen)

        self.draw_total(screen)

        if self.completed:
            self.draw_next(screen)

        self.draw_help_ui(screen)

        if self.tutorial_ui is not None:
            self.tutorial_ui.draw(screen)

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

        descGoalFontSize = 12 if self.current_world == 4 else 40
        self.desc_goal = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                          descGoalFontSize).render(binary_str, True, color)
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
        surf = pygame.Surface((150, 80), pygame.SRCALPHA)

        buttonImage = pygame.image.load(resource_path('./res/NextLevelButton.png'))
        surf.blit(buttonImage, pygame.Rect(0, 0, 150, 80))

        next_button_text = pygame.font.Font(resource_path(
            './res/TTOctosquaresTrialRegular.ttf'), 42).render("Next", True, (0, 0, 0))
        text_rect = next_button_text.get_rect(center=surf.get_rect().center)
        surf.blit(next_button_text, text_rect)
        screen.blit(surf, self.next_button_rect)

    # ==============================================================================================================
    # State management
    # ==============================================================================================================

    def onEnterState(self, payload: InGameStatePayload) -> None:
        pathStr = resource_path(f"res/worlds/{payload.world}/{payload.level}.json")

        self.current_world = payload.world
        self.current_level = payload.level
        self.level = load_level(pathStr)

        self.tutorial_ui = None
        if self.current_world == 0 and self.current_level == 1:
            self.tutorial_ui = TutorialUi(self)

        self.current_answer: float | None = None
        self.selected_card: CardUi | None = None
        self.mouse_click_offset = (0, 0)

        self.init_card_slots()

        if (self.cutsceneManager.queuedCutscene != payload.world):
            self.cutsceneManager.QueueCutscene(payload.world)

        self.help_ui = HelpUi(self.level.hint)
        self.sand_ui = SandUi(self.current_world)

    def onExitState(self) -> None:
        pygame.mixer.music.load(resource_path('./res/TitleTheme.mp3'))
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)

    def init_card_slots(self):
        self.card_slots: list[CardSlotUi] = []
        self.cards_ui: list[CardUi] = []

        goalFontSize = 40 if self.current_world == 4 else 128
        self.goal_text = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                          goalFontSize).render(f'{(2 ** self.level.nb_bits_to_overflow) - 1:,}', True, (255, 255, 255))
        self.goal_rect = self.goal_text.get_rect(center=self.game.screen.get_rect().center)
        self.goal_rect.y = 40 if self.current_world == 4 else -20  # 1/18 * self.game.screen.get_rect().h

        self.world_text = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'),
                                           32).render('World ' + str(self.current_world) + ' Level ' + str(self.current_level), True, (255, 255, 255))
        self.world_rect = self.world_text.get_rect(bottomright=self.game.screen.get_rect().bottomright)
        self.world_rect.x -= 15
        self.world_rect.y -= 10

        self.next_button_rect = pygame.Rect(self.game.screen.get_rect().right - 200,
                                            self.game.screen.get_rect().bottom - 150, 150, 80)

        pygame.mixer.music.load(resource_path('./res/MainThemeV4.mp3'))
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)
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


TUTORIAL_STEPS = [
    "This is the target you need to overflow, which means you need a bigger number than this",
    "Those are the cards you can combine to overflow the target",
    "Drag or double-click the cards in these slots to make an equation",
    "The evaluated equation will show up here along with it's binary representation",
    '''The key "R" resets the board. If you need help, click on the '?' button to get an hint. Good luck!'''
]


class TutorialUi:
    def __init__(self, game_state: InGameState):
        self.game_state = game_state
        self.font = pygame.font.Font(resource_path('./res/TTOctosquaresTrialRegular.ttf'), 18)
        self.current_step = 0

        self.cur_rect: pygame.Rect | None = None

    def redraw_surf(self):
        self.surf = pygame.image.load(resource_path('./res/TextboxTutorial.png')).convert_alpha()

        button = pygame.Surface((75, 25))
        button.fill((0, 171, 255))

        self.button_rect = button.get_rect(center=(self.surf.get_rect().centerx, self.surf.get_rect().bottom - 25))
        next_surf = self.font.render("Next", True, (255, 255, 255))

        button.blit(next_surf, next_surf.get_rect(center=button.get_rect().center))

        self.surf.blit(button, self.button_rect)

    def on_click(self, pos: tuple[int, int]):
        if self.cur_rect is None:
            return

        rect = self.cur_rect.move(self.button_rect.topleft)

        if rect.collidepoint(pos):
            self.current_step = self.current_step + 1
            if self.current_step >= len(TUTORIAL_STEPS):
                self.current_step = -1

    def draw(self, screen):
        self.redraw_surf()

        width, height = self.surf.get_size()

        topleftx = screen.get_rect().width - width - 50

        if self.current_step < 0:
            return
        if self.current_step == 0:
            toplefty = self.game_state.goal_rect.centery - height // 2
        elif self.current_step == 1:
            toplefty = self.game_state.cards_ui[0].rect.centery - height // 2
        elif self.current_step == 2:
            toplefty = self.game_state.card_slots[0].rect.centery - height // 2
        elif self.current_step == 3:
            toplefty = self.game_state.total_rect.centery - height // 2
        elif self.current_step == 4:
            topleftx = self.game_state.help_btn_rect.topleft[0]
            toplefty = self.game_state.help_btn_rect.topleft[1] - height - 10

        self.cur_rect = self.surf.get_rect(topleft=(topleftx, toplefty))

        drawText(self.surf, TUTORIAL_STEPS[self.current_step], (0, 0, 0),
                 self.surf.get_rect().inflate(-20, -20), self.font)

        screen.blit(self.surf, self.cur_rect)


def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text
