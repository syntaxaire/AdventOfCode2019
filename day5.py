"""Problem statement: https://adventofcode.com/2019/day/5"""
from typing import List

from Intcode import IntcodeVM


def decode_opcode(value: int) -> list:
    """Return a list with the opcode, and parameter modes that were encoded in value.

    Example: 1002 (01002) will return [2, 0, 1, 0] for the opcode and three parameter modes."""
    svalue = str(value)
    if len(svalue) <= 2:
        return [value]
    opcode = int(svalue[-2:])
    svalue = reversed(svalue[:-2])
    return [int(opcode)] + [int(val) for val in list(svalue)]


def run_intcode(memory: List[int], inputs: list, outputs: list):
    """Run the Intcode VM on the contents of memory, consuming inputs and writing to outputs.

    memory, inputs and outputs will be mutated."""
    ip = 0  # instruction pointer
    decode = decode_opcode(memory[ip])
    opcode = decode.pop(0)  # remainder, if any, is parameter modes
    while opcode != HALT:
        if opcode == ADD:
            mode = decode.pop(0)
            if mode == POSITION:
                operand_a = memory[memory[ip + 1]]
            elif mode == IMMEDIATE:
                operand_a = memory[ip + 1]
            mode = decode.pop(0)
            if mode == POSITION:
                operand_b = memory[memory[ip + 2]]
            elif mode == IMMEDIATE:
                operand_b = memory[ip + 1]
            target = memory[ip + 3]
            memory[target] = operand_a + operand_b
            increment = 4
        elif opcode == MULTIPLY:
            operand_a = memory[memory[ip + 1]]
            operand_b = memory[memory[ip + 2]]
            target = memory[ip + 3]
            memory[target] = operand_a * operand_b
            increment = 4
        elif opcode == STORE:
            value = inputs.pop(0)
            target = memory[ip + 1]
            memory[target] = value
            increment = 2
        elif opcode == RETRIEVE:
            source = memory[ip + 1]
            outputs.append(memory[source])
            increment = 2
        ip += increment
        decode = decode_opcode(memory[ip])
        opcode = decode.pop(0)  # remainder, if any, is parameter modes


if __name__ == '__main__':
    print(extract_opcode(103002))
