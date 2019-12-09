from typing import List, Tuple

# opcodes for the Intcode machine
ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMPIFTRUE = 5
JUMPIFFALSE = 6
LESSTHAN = 7
EQUALS = 8
HALT = 99

# sequence lengths for the Intcode machine, including the opcode itself
OPCODE_LENGTHS = {ADD: 4,
                  MULTIPLY: 4,
                  INPUT: 2,
                  OUTPUT: 2,
                  HALT: 1,
                  JUMPIFTRUE: 3,
                  JUMPIFFALSE: 3,
                  LESSTHAN: 4,
                  EQUALS: 4,
                  }

# parameter modes for the Intcode machine
POSITION = 0
IMMEDIATE = 1


class IntcodeVM:
    def __init__(self, memory: List[int], inputs: list, outputs: list, debug=False):
        self.memory = memory
        self.inputs = inputs
        self.outputs = outputs
        self.debug = debug

    def decode(self, addr) -> Tuple[int, List[int]]:
        """Return the opcode at the given address, and the list of parameter modes it may need to
        operate. Fills any parameter mode that is not explicitly given with the default."""
        instruction = str(self.memory[addr])  # e.g. '1002'
        opcode = int(instruction[-2:])
        remainder = list(instruction[:-2])  # may be [] if a bare opcode was given (e.g. '2')
        num_params = OPCODE_LENGTHS[opcode] - 1  # -1 for the opcode itself
        modes = []
        while num_params > 0:
            try:
                modes.append(int(remainder.pop()))
            except IndexError:
                # no more modes were given in the instruction, so use the position mode default
                modes.append(POSITION)
            num_params -= 1
        return opcode, modes

    def read(self, addr, mode=IMMEDIATE) -> int:
        """Read from memory at the given address, using the given mode."""
        if mode == POSITION:  # dereference a pointer
            return self.memory[self.memory[addr]]
        elif mode == IMMEDIATE:
            return self.memory[addr]

    def run(self):
        ip = 0
        jumped = False
        opcode, modes = self.decode(ip)
        while opcode != HALT:  # code 99
            if opcode == ADD:  # code 1
                a = self.read(ip+1, modes.pop(0))
                b = self.read(ip+2, modes.pop(0))
                addr = self.read(ip+3)
                self.memory[addr] = a + b
            elif opcode == MULTIPLY:  # code 2
                a = self.read(ip+1, modes.pop(0))
                b = self.read(ip+2, modes.pop(0))
                addr = self.read(ip+3)
                self.memory[addr] = a * b
            elif opcode == INPUT:  # code 3
                addr = self.read(ip+1)
                val = self.inputs.pop(0)
                self.memory[addr] = val
            elif opcode == OUTPUT:  # code 4
                val = self.read(ip+1, modes.pop(0))
                self.outputs.append(val)
            elif opcode == JUMPIFTRUE:  # code 5
                val = self.read(ip+1, modes.pop(0))
                addr = self.read(ip+2, modes.pop(0))
                if val != 0:
                    ip = addr
                    jumped = True
            elif opcode == JUMPIFFALSE:  # code 6
                val = self.read(ip+1, modes.pop(0))
                addr = self.read(ip+2, modes.pop(0))
                if val == 0:
                    ip = addr
                    jumped = True
            elif opcode == LESSTHAN:  # code 7
                a = self.read(ip+1, modes.pop(0))
                b = self.read(ip+2, modes.pop(0))
                addr = self.read(ip+3)
                if a < b:
                    self.memory[addr] = 1
                else:
                    self.memory[addr] = 0
            elif opcode == EQUALS:  # code 8
                a = self.read(ip + 1, modes.pop(0))
                b = self.read(ip + 2, modes.pop(0))
                addr = self.read(ip + 3)
                if a == b:
                    self.memory[addr] = 1
                else:
                    self.memory[addr] = 0
            if not jumped:
                ip += OPCODE_LENGTHS[opcode]
            else:
                jumped = False
            opcode, modes = self.decode(ip)
