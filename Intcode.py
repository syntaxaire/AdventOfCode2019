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
SETRELATIVEBASE = 9
HALT = 99

# sequence lengths for the Intcode machine, including the opcode itself
OPCODE_LENGTHS = {ADD: 4,
                  MULTIPLY: 4,
                  INPUT: 2,
                  OUTPUT: 2,
                  JUMPIFTRUE: 3,
                  JUMPIFFALSE: 3,
                  LESSTHAN: 4,
                  EQUALS: 4,
                  SETRELATIVEBASE: 2,
                  HALT: 1,
                  }

# parameter modes for the Intcode machine
POSITION = 0
IMMEDIATE = 1
RELATIVE = 2


class IntcodeVM:
    def __init__(self, memory: List[int], inputs: list):
        self.memory = memory
        self.inputs = inputs
        self.outputs = []
        self.ip = 0
        self.relativebase = 0
        self.halted = False

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
            if self.memory[addr] > len(self.memory):
                self.memory.extend([0] * (self.memory[addr] - len(self.memory) + 1))
            return self.memory[self.memory[addr]]
        elif mode == IMMEDIATE:
            return self.memory[addr]
        elif mode == RELATIVE:
            if addr + self.relativebase > len(self.memory):
                self.memory.extend([0] * (addr + self.relativebase - len(self.memory) + 1))
            return self.memory[addr + self.relativebase]

    def write(self, val, addr, mode=POSITION):
        """Write val to memory at the given address, using the given mode."""
        if addr + self.relativebase > len(self.memory):
            self.memory.extend([0] * (addr + self.relativebase))
        if mode == RELATIVE:
            self.memory[addr + self.relativebase] = val
        else:  # TODO: does this need support for IMMEDIATE and POSITION?
            self.memory[addr] = val

    def add_input(self, value: int):
        self.inputs.append(value)

    def run(self):
        """Run the virtual machine until it executes operation 99 (opcode HALT), then return the
        output list."""
        while True:
            try:
                next(self)
            except StopIteration:
                return self.outputs

    def __iter__(self):
        return self

    def __next__(self):
        """Run the virtual machine until it produces its next output."""
        opcode, modes = self.decode(self.ip)
        while True:
            if opcode == HALT:
                self.halted = True
                raise StopIteration
            if opcode == ADD:  # code 1
                a = self.read(self.ip + 1, modes[0])
                b = self.read(self.ip + 2, modes[1])
                target = self.read(self.ip + 3)
                self.write(a + b, target)
                self.ip += 4
            elif opcode == MULTIPLY:  # code 2
                a = self.read(self.ip + 1, modes[0])
                b = self.read(self.ip + 2, modes[1])
                target = self.read(self.ip + 3)
                self.write(a * b, target)
                self.ip += 4
            elif opcode == INPUT:  # code 3
                mode = modes.pop(0)
                target = self.read(self.ip + 1)
                val = self.inputs.pop(0)
                self.write(val, target, mode)
                self.ip += 2
            elif opcode == OUTPUT:  # code 4
                val = self.read(self.ip + 1, modes[0])
                self.outputs.append(val)
                self.ip += 2
                return val
            elif opcode == JUMPIFTRUE:  # code 5
                val = self.read(self.ip + 1, modes[0])
                addr = self.read(self.ip + 2, modes[1])
                if val != 0:
                    self.ip = addr
                else:
                    self.ip += 3
            elif opcode == JUMPIFFALSE:  # code 6
                val = self.read(self.ip + 1, modes[0])
                addr = self.read(self.ip + 2, modes[1])
                if val == 0:
                    self.ip = addr
                else:
                    self.ip += 3
            elif opcode == LESSTHAN:  # code 7
                a = self.read(self.ip + 1, modes[0])
                b = self.read(self.ip + 2, modes[1])
                target = self.read(self.ip + 3)
                if a < b:
                    self.write(1, target)
                else:
                    self.write(0, target)
                self.ip += 4
            elif opcode == EQUALS:  # code 8
                a = self.read(self.ip + 1, modes[0])
                b = self.read(self.ip + 2, modes[1])
                target = self.read(self.ip + 3)
                if a == b:
                    self.write(1, target)
                else:
                    self.write(0, target)
                self.ip += 4
            elif opcode == SETRELATIVEBASE:
                self.relativebase += self.read(self.ip + 1, modes[0])
                self.ip += 2
            opcode, modes = self.decode(self.ip)
