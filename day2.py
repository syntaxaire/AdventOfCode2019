"""Problem statement: https://adventofcode.com/2019/day/2"""
from typing import List

ADD = 1
MULTIPLY = 2
HALT = 99


def run_intcode(memory: List[int]):
    """Run the Intcode VM on the contents of memory."""
    instruction_pointer = 0
    while (opcode := memory[instruction_pointer]) != HALT:
        operand_a = memory[memory[instruction_pointer + 1]]
        operand_b = memory[memory[instruction_pointer + 2]]
        target = memory[instruction_pointer + 3]
        if opcode == ADD:
            memory[target] = operand_a + operand_b
        elif opcode == MULTIPLY:
            memory[target] = operand_a * operand_b
        instruction_pointer += 4


def run_tests():
    print("Tests:")
    tests = [[1, 0, 0, 0, 99],
             [2, 3, 0, 3, 99],
             [2, 4, 4, 5, 99, 0],
             [1, 1, 1, 4, 99, 5, 6, 0, 99]]
    for test in tests:
        start_memory = list(test)
        run_intcode(test)
        print(f'{start_memory} becomes {test}')


if __name__ == '__main__':
    # run_tests()
    # Solve part 1:
    with open('day2.input', 'r') as f:
        input_memory = [int(val) for val in f.read().split(',')]
    # Set up state for problem:
    input_memory[1] = 12
    input_memory[2] = 2
    memcopy = list(input_memory)
    run_intcode(memcopy)
    print("Part 1:")
    print(memcopy)

    # Solve part 2:
    for input1 in range(100):
        for input2 in range(100):
            memcopy = list(input_memory)
            memcopy[1] = input1
            memcopy[2] = input2
            run_intcode(memcopy)
            if memcopy[0] == 19690720:
                print(f'Part 2: {input1=} {input2=}')
