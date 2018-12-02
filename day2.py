from util import Input
from collections import Counter

# https://adventofcode.com/2018/day/2

# Part 1
words = [s.strip() for s in Input(2)]
doubles = 0
triples = 0

for word in words:
    c = Counter(word)
    if 2 in c.values():
        doubles += 1
    if 3 in c.values():
        triples += 1

print(doubles * triples)


# Part 2
def match(first, second):
    location = -1
    for i, c in enumerate(first):
        if first[i] != second[i]:
            if location != -1:
                return None
            location = i

    return second[:location] + second[location + 1:]

for i, first in enumerate(words):
    for second in words[i + 1:]:
        res = match(first, second)
        if res:
            print(res)
