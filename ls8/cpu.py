"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.op_size = 0

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0
        # program = [0] * 256

        
        print("using: cpu.py")
        with open(sys.argv[1]) as inst_file:
            for line in inst_file:
                split_cmds = line.split('#')[0].strip()
                if split_cmds == '':
                    continue
                inst_nums = int(split_cmds, 2)
                self.ram[address] = inst_nums
                address += 1
        
                    

        # For now, we've just hardcoded a program:
        # rewrite the program so it's dynamic
        # use argv and make sure there are 2 indexes (filename and user specified?)

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        is_running = True
        while is_running:
            cmd = self.ram_read(self.pc)
            if cmd == self.LDI:
                reg_index = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_index] = value
                self.op_size = 3
            elif cmd == self.PRN:
                reg_index = self.ram[self.pc + 1]
                print(self.reg[reg_index])
                self.op_size = 2
            elif cmd == self.HLT:
                is_running = False
                self.op_size = 1
            elif cmd == self.MUL:
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
            self.pc += self.op_size
