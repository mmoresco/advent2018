from util import Input
from collections import Counter
from collections import namedtuple

# https://adventofcode.com/2018/day/6

Cell = namedtuple("Cell", ["neighbor", "distance", "safe"])


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def parse(text):
    points = [tuple(int(x.strip()) for x in line.split(","))
              for line in text]

    # Grid is infinite, and grid[width][height] is a valid point
    width = max(points, key=lambda x: x[0])[0] + 1
    height = max(points, key=lambda x: x[1])[1] + 1
    grid = [[Cell(None, float("inf"), False) for _ in range(width)] for _ in range(height)]

    return points, grid


def get_neighbors(grid, point):
    height = len(grid)
    width = len(grid[0])
    x, y = point

    ret = []

    if x > 0:
        ret.append((x - 1, y))
    if y > 0:
        ret.append((x, y - 1))
    if x < width - 1:
        ret.append((x + 1, y))
    if y < height - 1:
        ret.append((x, y + 1))

    return ret


def flood_fill(grid, point, candidate):
    to_visit = set()
    to_visit.add(point)

    while to_visit:
        x, y = point = to_visit.pop()

        current_distance = grid[y][x].distance
        candidate_distance = distance(candidate, point)

        if candidate_distance > current_distance:
            continue
        elif candidate_distance < current_distance:
            grid[y][x] = Cell(candidate, candidate_distance, False)
        elif grid[y][x].neighbor in (candidate, '.'):
            continue
        elif candidate_distance == current_distance:
            grid[y][x] = Cell('.', current_distance, False)

        to_visit.update(get_neighbors(grid, point))


def get_border_points(grid):
    ret = []
    width = len(grid[0])
    height = len(grid)

    for y in range(height):
        ret.append((0, y))
        ret.append((width - 1, y))

    for x in range(width):
        ret.append((x, 0))
        ret.append((x, height - 1))

    return ret


def is_safe(i, j, points):
    boundary = 10000
    total = 0

    for x, y in points:
        total += distance((x, y), (j, i))
        if total >= boundary:
            return False
    return True


def mark_safe(grid, points):
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if is_safe(i, j, points):
                grid[i][j] = grid[i][j]._replace(safe=True)


text = Input(6).readlines()
points, grid = parse(text)

for point in points:
    flood_fill(grid, point, point)

areas = Counter([item.neighbor for row in grid for item in row])
border_points = get_border_points(grid)
for x, y in border_points:
    del areas[grid[y][x].neighbor]

# Part 1
print(max(areas.values()))

# Part 2
mark_safe(grid, points)
safe_areas = Counter([item.safe for row in grid for item in row])
print(safe_areas[True])
