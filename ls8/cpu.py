"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = []

        with open(filename) as f:
            program = f.readlines()
        for line in program:
            if '#' in line:
                instruction = line.split('#')[0]
            else:
                instruction = line.split('\n')[0]
            if len(instruction) == 0:
                continue
            else:
                instruction = int(instruction, 2)
                self.ram_write(instruction, address)
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif: op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def decode(self, bite):
        dictionary = {
            0b10100000: 'ADD',
            0b10101000: 'AND',
            0b01010000: 'CALL',
            0b10100111: 'CMP',
            0b01100110: 'DEC',
            0b10100011: 'DIV',
            0b00000001: 'HLT',
            0b01100101: 'INC',
            0b01010010: 'INT',
            0b00010011: 'IRET',
            0b01010101: 'JEQ',
            0b01011010: 'JGE',
            0b01010111: 'JGT',
            0b01011001: 'JLE',
            0b01011000: 'JLT',
            0b01010100: 'JMP',
            0b01010110: 'JNE',
            0b10000011: 'LD',
            0b10000010: 'LDI',
            0b10100100: 'MOD',
            0b10100010: 'MUL',
            0b00000000: 'NOP',
            0b01101001: 'NOT',
            0b10101010: 'OR',
            0b01000110: 'POP',
            0b01001000: 'PRA',
            0b01000111: 'PRN',
            0b01000101: 'PUSH',
            0b00010001: 'RET',
            0b10101100: 'SHL',
            0b10101101: 'SHR',
            0b10000101: 'ST',
            0b10100001: 'SUB',
            0b10101011: 'XOR'
        }

        return dictionary[bite]

    def run(self):
        running = True
        while running:
            ir = self.ram_read(self.pc)
            inst = self.decode(ir)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            is_alu = ir >> 5 & 1

            if inst == 'HLT':
                running = False
            elif is_alu:
                self.alu(inst, operand_a, operand_b)
            elif inst == 'LDI':
                self.reg[operand_a] = operand_b
            elif inst == 'PRN':
                print(self.reg[operand_a])

            inst_len = ir >> 6 & 0b11
            self.pc += inst_len+1
