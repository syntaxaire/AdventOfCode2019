from typing import List, Tuple

# opcodes for the Intcode machine
ADD = 1
MULTIPLY = 2
STORE = 3
RETRIEVE = 4
HALT = 99

# sequence lengths for the Intcode machine, including the opcode itself
OPCODE_LENGTHS = {ADD: 4,
                  MULTIPLY: 4,
                  STORE: 2,
                  RETRIEVE: 2,
                  HALT: 1,
                  }

# parameter modes for the Intcode machine
POSITION = 0
IMMEDIATE = 1


class IntcodeVM:
    def __init__(self, memory: List[int], inputs: list, outputs: list):
        self.memory = memory
        self.inputs = inputs
        self.outputs = outputs

    def decode(self, addr) -> Tuple[int, List[int]]:
        """Return the opcode at the given address, and the list of modes it needs to operate."""
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
        opcode, modes = self.decode(ip)
        while opcode != HALT:
            if opcode == ADD:
                a = self.read(ip+1, modes.pop(0))
                b = self.read(ip+2, modes.pop(0))
                addr = self.read(ip+3)
                self.memory[addr] = a + b
            elif opcode == MULTIPLY:
                a = self.read(ip+1, modes.pop(0))
                b = self.read(ip+2, modes.pop(0))
                addr = self.read(ip+3)
                self.memory[addr] = a * b
            elif opcode == STORE:
                addr = self.read(ip+1)
                self.memory[addr] = self.inputs.pop(0)
            elif opcode == RETRIEVE:
                addr = self.read(ip+1)
                self.outputs.append(self.memory[addr])
            ip += OPCODE_LENGTHS[opcode]
            opcode, modes = self.decode(ip)
