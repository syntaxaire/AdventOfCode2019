"""Problem statement: https://adventofcode.com/2019/day/3"""
from typing import List


def layout_wire(instructions: List[str]) -> List[tuple]:
    """Lay out a wire on the grid, according to instructions, starting at (0, 0). Return a list of
    the coordinates the wire touches, in order.

    The instructions given are strings like 'L8' and 'U20', a letter direction followed by an
    integer."""
    walk = []
    x, y = 0, 0
    for instruction in instructions:
        direction, length = instruction[0], int(instruction[1:])
        if direction == 'R':
            for x in range(x+1, x+1+length):
                walk.append((x, y))
        elif direction == 'L':
            for x in range(x-1, x-1-length, -1):
                walk.append((x, y))
        elif direction == 'U':
            for y in range(y+1, y+1+length):
                walk.append((x, y))
        elif direction == 'D':
            for y in range(y-1, y-1-length, -1):
                walk.append((x, y))
    return walk


def length_to_coord(layout: List[tuple], coord: tuple) -> int:
    """Return the distance a wire with the given layout travels to get to the given coordinates."""
    length = 0
    for location in layout:
        length += 1
        if location == coord:
            return length
    raise ValueError('The wire did not reach the given coordinates')


def solve_part1(wire_a: List[str], wire_b: List[str]) -> int:
    """Solve part 1 of the problem:

    Return the Manhattan distance from the central port to the closest intersection."""
    a_walk = layout_wire(wire_a)
    b_walk = layout_wire(wire_b)
    a_coords = set(a_walk)
    b_coords = set(b_walk)
    intersections = a_coords.intersection(b_coords)
    lowest = 1_000_000
    for x, y in intersections:
        combined_distance = abs(x) + abs(y)
        if combined_distance < lowest:
            lowest = combined_distance
    return lowest


def solve_part2(wire_a: List[str], wire_b: List[str]) -> int:
    """Solve part 2 of the problem:

    Return the fewest combined steps the wires must take to reach an intersection."""
    a_walk = layout_wire(wire_a)
    b_walk = layout_wire(wire_b)
    a_coords = set(a_walk)
    b_coords = set(b_walk)
    intersections = a_coords.intersection(b_coords)
    lengths = {}
    for intersection in intersections:
        a_length_to = length_to_coord(a_walk, intersection)
        b_length_to = length_to_coord(b_walk, intersection)
        lengths[intersection] = (a_length_to, b_length_to)
    lowest = 1_000_000_000
    for intersection, lengthpair in lengths.items():
        x, y = lengthpair
        combined_distance = x + y
        if combined_distance < lowest:
            lowest = combined_distance
    return lowest


if __name__ == '__main__':
    with open('day3.input', 'r') as f:
        a = f.readline().split(',')
        b = f.readline().split(',')
    answer = solve_part1(a, b)
    print(f'The Manhattan distance from the central port to the closest intersection is {answer}.')
    answer = solve_part2(a, b)
    print(f'The fewest combined steps the wires must take to reach an intersection is {answer}.')
