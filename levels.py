import json
from dataclasses import dataclass
from math import nan

from sympy import sympify

VALID_CHARACTERS = ['+', '-', '*', '/', '!', '(', ')', '^']


@dataclass
class Level:
    nbBitsToOverflow: int
    characters: list[str]
    minCharacters: int
    maxCharacters: int


def load_level(level_path: str) -> Level:
    with open(level_path) as f:
        level_json = json.load(f)

        if 'nbBitsToOverflow' not in level_json:
            raise ValueError(f'nbBitsToOverflow not found in level {level_path}')
        if 'characters' not in level_json:
            raise ValueError(f'characters not found in level {level_path}')

        nbBitsToOverflow = int(level_json['nbBitsToOverflow'])
        if nbBitsToOverflow < 1:
            raise ValueError(f'Invalid nbBitsToOverflow for level {level_path}: {nbBitsToOverflow}')

        characters = level_json['characters']
        for character in characters:
            if not character.isnumeric() and not character in VALID_CHARACTERS:
                raise ValueError(f'Invalid character found for level {level_path}: {character}')

        minCharacters = 0
        maxCharacters = len(characters)
        if 'minCharacters' in level_json:
            minCharacters = int(level_json['minCharacters'])
        if 'maxCharacters' in level_json:
            maxCharacters = int(level_json['maxCharacters'])

        if minCharacters < 0 or minCharacters > len(characters):
            raise ValueError(f'Invalid minCharacters for level {level_path}: {minCharacters}')

        if maxCharacters <= 0 or maxCharacters > len(characters):
            raise ValueError(f'Invalid maxCharacters for level {level_path}: {maxCharacters}')

        if minCharacters > maxCharacters:
            raise ValueError(f'minCharacters is greater than maxCharacters for level {level_path}')

        level = Level(nbBitsToOverflow, characters, minCharacters, maxCharacters)

    return level


def is_solution_valid(level: Level, solution: list[str]) -> tuple[bool, float]:
    # Validate length of expression
    expression = ''.join(solution)
    if len(expression) < level.minCharacters or len(expression) > level.maxCharacters:
        return False, nan

    # Validate characters in expression
    solution_characters = level.characters.copy()
    for character in solution:
        if character not in solution_characters:
            raise ValueError(f'Invalid character found in solution: {character}')

        solution_characters.remove(character)

    try:
        value = sympify(expression)
    except:
        return False, nan

    # Check if value actually overflows
    return value > 2**level.nbBitsToOverflow-1, value


if __name__ == '__main__':
    level = load_level('res/levels/7.json')

    print(f'Number to overflow: {2**level.nbBitsToOverflow-1}')
    print(f'Characters: {level.characters}')
    print(f'Nb characters constraints: [{level.minCharacters},{level.maxCharacters}]')

    running = True
    while running:
        solution = input('Enter your solution : ')
        is_valid, value = is_solution_valid(level, list(solution))
        print(f'Result is: {value}')

        running = not is_valid
