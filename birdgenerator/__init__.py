import random
from pathlib import Path

_dir = Path(__file__).parent


def _load(name):
    return [x.strip() for x in (_dir / name).read_text().splitlines()]


colors = _load('colors.txt')
locations = _load('locations.txt')
names = _load('names.txt')
parts = _load('parts.txt')
adjectives = _load('adjectives.txt')


def _generate_new_name():
    if random.uniform(0, 1) > 0.5:
        half1 = random.choice(names)
        half2 = random.choice(names)
        if half1 == half2:
            return half1
        name = half1[0:_find_next_vowel(half1, int(len(half1) / 2))] + half2[int(len(half2) / 2):len(half2)]
        return name
    return random.choice(names)


def _find_next_vowel(str, i):
    for x in range(i, len(str)):
        if str[x] in ('a', 'e', 'i', 'o', 'u', 'y'):
            return x + 1
    return i


def generate_bird(seed):
    name = ''
    hascolor = False
    haspart = False
    haslocation = False

    random.seed(seed)

    if random.uniform(0, 1) > 0.25:  # add colors
        name += random.choice(colors).capitalize() + ' '
        hascolor = True
        if random.uniform(0, 1) > 0.5:  # add part
            name += random.choice(parts).capitalize() + ' '
            haspart = True
    if not hascolor or random.uniform(0, 1) > 0.5:  # add location
        name += random.choice(locations) + ' '
        haslocation = True
    if random.uniform(0, 1) > 0.75:
        name += random.choice(adjectives).capitalize() + ' '
    elif haspart and random.uniform(0, 1) > 0.5:  # add colors again
        name += random.choice(colors).capitalize()
        if haslocation or random.uniform(0, 1) > 0.5:
            name += ' '
    name += _generate_new_name().capitalize()
    return name
