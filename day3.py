from util import Input
from collections import namedtuple, Counter

# https://adventofcode.com/2018/day/3


class Claim:
    def __init__(self, label, left, top, width, height):
        self.label = label
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        
        self.pixels = self.get_pixels()

    def get_pixels(self):
        pixels = []
        x = self.left
        y = self.top

        for i in range(self.width):
            for j in range(self.height):
                pixels.append(str(i + x) + "," + str(j + y))

        return pixels


def parse(lines):
    claims = []

    for line in lines:
        label, contents = line.split("@")
        location, size = contents.split(":")
        left, top = [int(n) for n in location.strip().split(',')]
        width, height = [int(n) for n in size.strip().split("x")]
        claim = Claim(label, left, top, width, height)
        claims.append(claim)

    return claims


def get_overlaps(claims):
    claimed = Counter()
    overlaps = 0

    for claim in claims:
        for pixel in claim.pixels:
            claimed[pixel] += 1
            if claimed[pixel] == 2:
                overlaps += 1

    return overlaps

test_claim_1 = Claim("first", 1, 3, 4, 4)
test_claim_2 = Claim("second", 3, 1, 4, 4)
test_claim_3 = Claim("third", 5, 5, 2, 2)
assert test_claim_1.pixels == ['1,3', '1,4', '1,5', '1,6',
                                    '2,3', '2,4', '2,5', '2,6',
                                    '3,3', '3,4', '3,5', '3,6',
                                    '4,3', '4,4', '4,5', '4,6']
assert test_claim_2.pixels == ['3,1', '3,2', '3,3', '3,4',
                                    '4,1', '4,2', '4,3', '4,4',
                                    '5,1', '5,2', '5,3', '5,4',
                                    '6,1', '6,2', '6,3', '6,4']
assert get_overlaps([test_claim_1, test_claim_2, test_claim_3]) == 4

claims = parse(Input(3))

# Part 1
print(get_overlaps(claims))


# Part 2
def find_overlapless(claims):
    claimed = Counter()

    # Build claim map
    for claim in claims:
        for pixel in claim.pixels:
            claimed[pixel] += 1

    for claim in claims:
        candidate = True
        for pixel in claim.pixels:
            if claimed[pixel] > 1:
                candidate = False
                break
        if candidate:
            return claim.label

    return None


print(find_overlapless(claims))