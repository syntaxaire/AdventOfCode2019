"""Problem statement: https://adventofcode.com/2019/day/2"""
from Intcode import IntcodeVM

# Solve part 1:
with open('day2.input', 'r') as f:
    orig_program = [int(val) for val in f.read().split(',')]
# Set up state for problem:
program = list(orig_program)  # we need the original program again for part 2, so copy it
program[1] = 12
program[2] = 2
vm = IntcodeVM(program, [], [])
vm.run()
print(f"The result of the program is {program[0]}.")

# Solve part 2:
for noun in range(100):
    for verb in range(100):
        program = list(orig_program)
        program[1] = noun
        program[2] = verb
        vm = IntcodeVM(program, [], [])
        vm.run()
        if program[0] == 19690720:
            print(f'The noun and verb that produce 19690720 are {noun=} and {verb=}.')
