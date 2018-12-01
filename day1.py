from util import Input

# https://adventofcode.com/2018/day/1


def parse(lines):
    return [int(n) for n in lines]


def find_repeat(deltas):
    seen = set()
    freq = 0

    while True:
        for change in deltas:
            if freq in seen:
                return freq

            seen.add(freq)
            freq += change


changes = parse(Input(1))

# Part 1
print(sum(changes))

# Part 2
print(find_repeat(changes))