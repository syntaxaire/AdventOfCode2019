"""Problem statement: https://adventofcode.com/2019/day/3"""

with open('day6.input', 'r') as f:
    orbits_input = f.readlines()
orbits = {}
for orbit in orbits_input:
    orbit = orbit.strip()
    center, obj = orbit.split(')')
    orbits[obj] = center

def count_orbits(mapping, obj):
    if mapping[obj] == 'COM':
        return 1
    return 1 + count_orbits(mapping, mapping[obj])

total_orbits = 0
for obj in orbits:
    total_orbits += count_orbits(orbits, obj)
print(total_orbits)


def get_chain(mapping, obj):
    chain = []
    loc = mapping[obj]
    while loc != 'COM':
        chain.append(loc)
        loc = mapping[loc]
    chain.append('COM')
    return list(reversed(chain))

my_chain = get_chain(orbits, 'YOU')
san_chain = get_chain(orbits, 'SAN')
print(my_chain)
print(san_chain)

while my_chain[0] == san_chain[0]:
    my_chain.pop(0)
    san_chain.pop(0)

print(my_chain)
print(san_chain)
print(len(my_chain) + len(san_chain))