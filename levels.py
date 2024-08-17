import json
from dataclasses import dataclass

from sympy import sympify

VALID_CARD_VALUES = ['+', '-', '*', '/', '!', '(', ')', '^', 'exp', 'log',
                     'ln', 'sqrt', 'pi', 'abs', 'e', 'sin', 'cos', 'tan']


@dataclass
class Card:
    value: str


@dataclass
class Level:
    nbBitsToOverflow: int
    cards: list[Card]
    minCards: int
    maxCards: int


def is_float(string):
    try:
        float(eval(string))
        return True
    except:
        return False


def load_level(level_path: str) -> Level:
    with open(level_path) as f:
        level_json = json.load(f)

        if 'nbBitsToOverflow' not in level_json:
            raise ValueError(f'nbBitsToOverflow not found in level {level_path}')
        if 'cards' not in level_json:
            raise ValueError(f'cards not found in level {level_path}')

        nbBitsToOverflow = int(level_json['nbBitsToOverflow'])
        if nbBitsToOverflow < 1:
            raise ValueError(f'Invalid nbBitsToOverflow for level {level_path}: {nbBitsToOverflow}')

        raw_cards = level_json['cards']
        for raw_card in raw_cards:
            if not is_float(raw_card) and not raw_card in VALID_CARD_VALUES:
                raise ValueError(f'Invalid card found for level {level_path}: {raw_card}')

        cards = [Card(raw_card) for raw_card in raw_cards]

        minCards = 0
        maxCards = len(cards)
        if 'minCards' in level_json:
            minCards = int(level_json['minCards'])
        if 'maxCards' in level_json:
            maxCards = int(level_json['maxCards'])

        if minCards < 0 or minCards > len(cards):
            raise ValueError(f'Invalid minCards for level {level_path}: {minCards}')

        if maxCards <= 0 or maxCards > len(cards):
            raise ValueError(f'Invalid maxCards for level {level_path}: {maxCards}')

        if minCards > maxCards:
            raise ValueError(f'minCards is greater than maxCards for level {level_path}')

        level = Level(nbBitsToOverflow, cards, minCards, maxCards)

    return level


def solution_preprocess(solution: list[Card]) -> list[Card]:
    # Sympy preprocess
    for i in range(len(solution)):
        card = solution[i]

        if card.value == 'e':
            card.value = 'E'

    # For cards that are functions, assume next card is the argument LGTM for now
    # e.g. 'sqrt' -> 'sqrt(' + next_card + ')'
    processed_solution = []
    i = 0
    while i < len(solution):
        card = solution[i]

        if i >= len(solution) - 1:
            processed_solution.append(card)
            continue

        if card.value == 'sqrt':
            card.value = 'sqrt('
        elif card.value == 'exp':
            card.value = 'exp('
        elif card.value == 'log':
            card.value = 'log(10,'
        elif card.value == 'ln':
            card.value = 'ln('
        elif card.value == 'abs':
            card.value = 'abs('
        elif card.value == 'sin':
            card.value = 'sin('
        elif card.value == 'cos':
            card.value = 'cos('
        elif card.value == 'tan':
            card.value = 'tan('
        else:
            processed_solution.append(card)
            i += 1
            continue

        next_card = solution[i + 1]

        processed_solution.append(card)
        processed_solution.append(next_card)
        processed_solution.append(Card(')'))

        i += 2

    return processed_solution


def evaluate_solution(level: Level, solution: list[Card]) -> float:
    # Validate length of expression
    if len(solution) < level.minCards or len(solution) > level.maxCards:
        raise ValueError(f'Invalid length of solution: {len(solution)}')

    # Validate cards in expression
    solution_cards = [card.value for card in level.cards]
    for card in solution:
        if card.value not in solution_cards:
            raise ValueError(f'Invalid card found in solution: {card}')

        solution_cards.remove(card.value)

    # Preprocess solution
    preprocessed_solution = solution_preprocess(solution)

    expression = ''.join([card.value for card in preprocessed_solution])
    print(expression)
    try:
        value = sympify(expression)
    except:
        raise ValueError(f'Invalid expression: {expression}')

    return value


if __name__ == '__main__':
    level_to_load = input('Enter the level to load: ')

    level = load_level(f'res/levels/{level_to_load}.json')

    cards_str = ', '.join([card.value for card in level.cards])

    print(f'Number to overflow: {2**level.nbBitsToOverflow-1}')
    print(f'Cards: {cards_str}')
    print(f'Nb cards constraints: [{level.minCards},{level.maxCards}]')

    running = True
    while running:
        solution_str = input('Enter your solution with each card separated by a comma : ')

        card_values = solution_str.replace(' ', '').split(',')
        cards = [Card(value) for value in card_values]

        try:
            value = evaluate_solution(level, cards)
        except Exception as e:
            print(e)
            continue

        print(f'Result is: {value}')

        running = value <= 2**level.nbBitsToOverflow-1

    print('You did it, gg!')
