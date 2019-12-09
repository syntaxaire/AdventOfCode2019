"""Problem statement: https://adventofcode.com/2019/day/5"""
from Intcode import IntcodeVM


def solve_part1(program):
    output = []
    vm = IntcodeVM(program, [1], output)
    vm.run()
    return output


def solve_part2(program):
    output = []
    vm = IntcodeVM(program, [5], output)
    vm.run()
    return output


def main():
    with open('day5.input', 'r') as f:
        orig_program = list(int(val) for val in f.read().split(','))
    program_copy = list(orig_program)
    answer1 = solve_part1(program_copy)
    print(f'The diagnostic tests returned {answer1[:-1]} (zeroes indicate passes).'
          f' The diagnostic code for input 1 was {answer1[-1]}.')
    program_copy = list(orig_program)
    answer2 = solve_part2(program_copy)
    print(f'The diagnostic code for input 5 was {answer2[-1]}.')


if __name__ == '__main__':
    main()
