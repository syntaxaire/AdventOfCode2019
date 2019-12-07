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
]


@pytest.mark.parametrize('program,after,inputs,outputs', TESTS)
def test_intcode_vm(program, after, inputs, outputs):
    vm = IntcodeVM(program, inputs, outputs)
    vm.run()
    print(program, after)
    assert program == after
