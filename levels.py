import json
from dataclasses import dataclass

import sympy
from sympy import sympify

VALID_CARD_VALUES = ['+', '-', '*', '/', '!', '(', ')', '^', 'exp', 'log',
                     'ln', 'sqrt', 'pi', 'abs', 'e', 'sin', 'cos', 'tan']


@dataclass
class Card:
    value: str


@dataclass
class Level:
    nb_bits_to_overflow: int
    cards: list[Card]
    min_cards: int
    max_cards: int


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

        nb_bits_to_overflow = int(level_json['nbBitsToOverflow'])
        if nb_bits_to_overflow < 1:
            raise ValueError(f'Invalid nbBitsToOverflow for level {level_path}: {nb_bits_to_overflow}')

        raw_cards = level_json['cards']
        for raw_card in raw_cards:
            if not is_float(raw_card) and not raw_card in VALID_CARD_VALUES:
                raise ValueError(f'Invalid card found for level {level_path}: {raw_card}')

        cards = [Card(raw_card) for raw_card in raw_cards]

        min_cards = 0
        max_cards = len(cards)
        if 'minCards' in level_json:
            min_cards = int(level_json['minCards'])
        if 'maxCards' in level_json:
            max_cards = int(level_json['maxCards'])

        if min_cards < 0 or min_cards > len(cards):
            raise ValueError(f'Invalid minCards for level {level_path}: {min_cards}')

        if max_cards <= 0 or max_cards > len(cards):
            raise ValueError(f'Invalid maxCards for level {level_path}: {max_cards}')

        if min_cards > max_cards:
            raise ValueError(f'minCards is greater than maxCards for level {level_path}')

        level = Level(nb_bits_to_overflow, cards, min_cards, max_cards)

    return level


def validate_solution(level: Level, solution: list[Card]) -> bool:
    # Validate length of expression
    if len(solution) < level.min_cards or len(solution) > level.max_cards:
        print(f'Invalid length of solution: {len(solution)}')
        return False

    # Validate cards in expression
    solution_cards = [card.value for card in level.cards]
    for card in solution:
        if card.value not in solution_cards:
            print(f'Invalid card found in solution: {card}')
            return False

        solution_cards.remove(card.value)

    # Check that we don't have two consecutive numerics
    for i in range(len(solution) - 1):
        a = solution[i].value
        b = solution[i + 1].value

        # This is to prevent two consecutive numerics which would lead to 1,1 => 11
        if is_float(a) and is_float(b):
            print(f'Two consecutive numerics found in solution: {solution[i].value}, {solution[i + 1].value}')
            return False
        # This is to prevent integer division
        if a == '/' and b == '/':
            print(f'Two consecutive division found in solution: {solution[i].value}, {solution[i + 1].value}')
            return False

    return True


def preprocess_solution(solution: list[Card]) -> list[Card]:
    # Sympy preprocess
    for card in solution:
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
            i += 1
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
    is_valid = validate_solution(level, solution)
    if not is_valid:
        raise ValueError('Solution validation failed')

    # Preprocess solution
    preprocessed_solution = preprocess_solution(solution)

    expression = ''.join([card.value for card in preprocessed_solution])
    try:
        value = sympify(expression).evalf()
    except:
        raise ValueError(f'Sympy evaluation failed for expression: {expression}')

    if value == sympy.zoo:
        raise ValueError('Division by zero')

    return value


if __name__ == '__main__':
    level_to_load = input('Enter the level to load: ')

    level = load_level(f'res/levels/{level_to_load}.json')

    cards_str = ', '.join([card.value for card in level.cards])

    print(f'Number to overflow: {2**level.nb_bits_to_overflow-1}')
    print(f'Cards: {cards_str}')
    print(f'Nb cards constraints: [{level.min_cards},{level.max_cards}]')

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

        running = value <= 2**level.nb_bits_to_overflow-1

    print('You did it, gg!')
