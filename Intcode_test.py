"""Tests for the IntcodeVM class in Intcode.py"""
import pytest

from Intcode import IntcodeVM

# These example programs consist of four lists each:
# The memory (program) before Intcode execution, the memory as it should look after execution,
# the input list before execution, and the output list as it should look after execution. Not all
# programs use input and output.

TESTS = [
    # day 2 examples, exercising opcodes 0, 1, and 99 (nicknamed ADD, MULTIPLY, and HALT)
    [[1, 0, 0, 3, 99], [1, 0, 0, 2, 99], [], []],
    [[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
     [], []],
    [[1, 0, 0, 0, 99], [2, 0, 0, 0, 99], [], []],
    [[2, 3, 0, 3, 99], [2, 3, 0, 6, 99], [], []],
    [[2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801], [], []],
    [[1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99], [], []],

    # day 5 examples, exercising opcodes 2 and 3 (nicknamed STORE and RETRIEVE), using input and
    # output, as well as the new parameter modes
    [[3, 0, 4, 0, 99], [999, 0, 4, 0, 99], [999], [999]],  # test input and output
    [[1002, 4, 3, 4, 33], [1002, 4, 3, 4, 99], [], []],
    [[1101, 100, -1, 4, 0], [1101, 100, -1, 4, 99], [], []],
    # day 5 examples, exercising opcodes 5, 6, 7, and 8 (nicknamed JUMPIFTRUE, JUMPIFFALSE,
    # LESSTHAN, and EQUALS)
    # output 1 if input equals 8 (using position mode):
    [[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [3, 9, 8, 9, 10, 9, 4, 9, 99, 0, 8], [7], [0]],
    [[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [3, 9, 8, 9, 10, 9, 4, 9, 99, 1, 8], [8], [1]],
    # output 1 if input less than 8 (using position mode):
    [[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [3, 9, 7, 9, 10, 9, 4, 9, 99, 1, 8], [7], [1]],
    [[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [3, 9, 7, 9, 10, 9, 4, 9, 99, 0, 8], [8], [0]],
    [[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [3, 9, 7, 9, 10, 9, 4, 9, 99, 0, 8], [9], [0]],
    # output 1 if input equals 8 (using immediate mode):
    [[3, 3, 1108, -1, 8, 3, 4, 3, 99], [3, 3, 1108, 0, 8, 3, 4, 3, 99], [7], [0]],
    [[3, 3, 1108, -1, 8, 3, 4, 3, 99], [3, 3, 1108, 1, 8, 3, 4, 3, 99], [8], [1]],
    # output 1 if input less than 8 (using immediate mode):
    [[3, 3, 1107, -1, 8, 3, 4, 3, 99], [3, 3, 1107, 1, 8, 3, 4, 3, 99], [7], [1]],
    [[3, 3, 1107, -1, 8, 3, 4, 3, 99], [3, 3, 1107, 0, 8, 3, 4, 3, 99], [8], [0]],
    [[3, 3, 1107, -1, 8, 3, 4, 3, 99], [3, 3, 1107, 0, 8, 3, 4, 3, 99], [9], [0]],
    # output 0 if input was zero, or 1 if input was nonzero (position mode):
    [[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
     [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, 0, 0, 1, 9], [0], [0]],
    [[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9],
     [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, 555, 1, 1, 9], [555], [1]],
    # output 0 if input was zero, or 1 if input was nonzero (immediate mode):
    [[3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],
     [3, 3, 1105, 0, 9, 1101, 0, 0, 12, 4, 12, 99, 0], [0], [0]],
    [[3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1],
     [3, 3, 1105, 555, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [555], [1]],
    # big example from day 5 part 2:
    # output 999 if input below 8, output 1000 if input equal to 8, output 1001 if input greater
    # than 8.
    [[3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
      1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
      999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99],
     [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
      1106, 0, 36, 98, 0, 7, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
      999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], [7], [999]],
    [[3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
      1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
      999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99],
     [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
      1106, 0, 36, 98, 1000, 8, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
      999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], [8], [1000]],
    [[3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
      1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
      999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99],
     [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
      1106, 0, 36, 98, 1001, 9, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
      999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99], [9], [1001]],
]


@pytest.mark.parametrize('program,want_memory,inputs,want_outputs', TESTS)
def test_intcode_vm(program, want_memory, inputs, want_outputs):
    outputs = []
    vm = IntcodeVM(list(program), inputs, outputs)
    vm.run()
    assert vm.memory == want_memory
    assert outputs == want_outputs
