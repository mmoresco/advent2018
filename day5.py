from util import Input
import string

# https://adventofcode.com/2018/day/5#part2

text = Input(5).read().strip()


def reduce(text):
    polymer = []
    for c in text:
        if polymer and c != polymer[-1] and c.lower() == polymer[-1].lower():
            polymer.pop()
        else:
            polymer.append(c)
    return len(polymer)

# Part 1
print(reduce(text))


# Part 2
def experiment(c):
    candidate = text.replace(c, '')
    candidate = candidate.replace(c.upper(), '')
    return reduce(candidate)

print(min(experiment(c) for c in string.ascii_lowercase))


