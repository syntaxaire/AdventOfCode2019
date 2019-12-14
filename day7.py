"""Problem statement: https://adventofcode.com/2019/day/7"""
import itertools

from Intcode import IntcodeVM


def solve_part1(program):
    permutations = itertools.permutations('01234')
    max_signal = 0
    for permutation in permutations:
        amp_settings = list(int(val) for val in permutation)
        signal = 0  # input for the first amplifier
        for _ in 'ABCDE':  # 'Amp A' through 'Amp E'
            program_copy = list(program)
            amplifier_phase_setting = amp_settings.pop()
            amplifier_input = [amplifier_phase_setting, signal]
            amplifier = IntcodeVM(program_copy, amplifier_input)
            signal = amplifier.run()[0]
        if signal > max_signal:
            max_signal = signal
    return max_signal


def solve_part2(program):
    permutations = itertools.permutations('56789')
    max_signal = 0
    for permutation in permutations:
        amp_lineup = [IntcodeVM(list(program), []) for _ in 'ABCDE']  # 'Amp A' through 'Amp E'
        amp_settings = list(int(val) for val in permutation)
        for amp in amp_lineup:
            amp.add_input(amp_settings.pop(0))  # provide amps with their configuration
        signal = 0  # input for the first amplifier
        finished = False
        while not finished:
            for amp in amp_lineup:
                amp.add_input(signal)
                try:
                    signal = next(amp)
                except StopIteration:
                    finished = True
        print(f'Output for {"".join(permutation)} was {signal}.')
        if signal > max_signal:
            max_signal = signal
    return max_signal


def main():
    with open('day7.input', 'r') as f:
        orig_program = list(int(val) for val in f.read().split(','))
    program_copy = list(orig_program)
    answer = solve_part1(program_copy)
    print(f'The highest signal that can be sent to the thrusters is {answer}.')

    program_copy = list(orig_program)
    answer2 = solve_part2(program_copy)
    print(f'Max signal was {answer2}.')


if __name__ == '__main__':
    main()
