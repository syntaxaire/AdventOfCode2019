"""Problem statement: https://adventofcode.com/2019/day/6"""


def build_orbit_mapping(lines):
    """Read lines in the format 'A)B' and return a dict mapping B:A."""
    mapping = {}
    for orbit in orbits_input:
        orbit = orbit.strip()
        center, outer = orbit.split(')')
        mapping[outer] = center
    return mapping


def count_orbits(mapping, outer):
    """Return the number of orbits linking this outer orbital body to the system's center."""
    if mapping[outer] == 'COM':
        return 1
    return 1 + count_orbits(mapping, mapping[outer])


def get_chain(mapping, outer):
    """Return a list of the orbital objects linking an outer object to the system's center."""
    chain = []
    loc = mapping[outer]
    while loc != 'COM':
        chain.append(loc)
        loc = mapping[loc]
    chain.append('COM')
    return list(chain)


if __name__ == '__main__':
    with open('day6.input', 'r') as f:
        orbits_input = f.readlines()
    orbits = build_orbit_mapping(orbits_input)
    total_orbits = 0
    for obj in orbits:
        total_orbits += count_orbits(orbits, obj)
    print(f'The number of direct plus indirect orbits in the system is {total_orbits}.')

    my_chain = get_chain(orbits, 'YOU')
    san_chain = get_chain(orbits, 'SAN')
    # find the point at which the orbital chains diverge:
    while my_chain[-1] == san_chain[-1]:
        my_chain.pop()
        san_chain.pop()
    transfers = len(my_chain) + len(san_chain)
    print(f'The number of orbital transfers between you and Santa is {transfers}.')
