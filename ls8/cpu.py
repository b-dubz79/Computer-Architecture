"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0,0,0,0,0,0,0,0xF4]
        self.pc = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.ADD = 0b10100000
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110
        self.eq_flag = 0b00000000
        


        # self.operations = {
        #     LDI: run_LDI
        # }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as inst_file:
            for line in inst_file:
                split_cmds = line.split('#')[0].strip()
                if split_cmds == '':
                    continue
                inst_nums = int(split_cmds, 2)
                self.ram[address] = inst_nums
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.eq_flag = 0b00000001
            else:
                self.eq_flag = 0b00000000
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
            # print('self  pc', self.pc)
            cmd = self.ram_read(self.pc)
            if cmd == self.LDI:
                reg_index = self.ram[self.pc + 1] # 00000001
                value = self.ram[self.pc + 2] # 00011000 (24!!)
                self.reg[reg_index]= value # R1 now holds 00011000 (mult2print)
                self.pc += 3 # LDI takes 2 operands (10 when bitshifted) 

            elif cmd == self.PUSH:
                self.reg[7] -= 1
                reg_index = self.ram[self.pc + 1]
                # get value of register @ reg_index and then put it into ram at current stack pointer
                # above comment goes right to left
                self.ram[self.reg[7]] = self.reg[reg_index]
                self.pc += 2

            elif cmd == self.POP:
                val = self.ram[self.reg[7]]
                reg_index = self.ram[self.pc + 1]
                self.reg[reg_index] = val
                self.reg[7] += 1
                self.pc += 2

            elif cmd == self.PRN:
                reg_index = self.ram[self.pc + 1]
                print(self.reg[reg_index])
                self.pc += 2

            elif cmd == self.HLT:
                is_running = False
                
            elif cmd == self.MUL:
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3
            elif cmd == self.ADD:
                self.alu("ADD", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3

            elif cmd == self.CMP:
                self.alu("CMP", self.ram[self.pc + 1], self.ram[self.pc + 2])
                # print('does it get here')
                self.pc += 3

            elif cmd == self.JEQ:
                self.reg[7] -= 1
                self.ram[self.reg[7]] = self.pc + 2
                # print('what about here')
                if self.eq_flag == True:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    self.pc += 2
                    
            elif cmd == self.JNE:
                self.reg[7] -= 1
                self.ram[self.reg[7]] = self.pc + 2
                # print('here?')
                if self.eq_flag == False:
                    self.pc = self.reg[self.ram[self.pc + 1]]
                else:
                    self.pc += 2

            elif cmd == self.JMP:
                self.reg[7] -= 1
                self.ram[self.reg[7]] == self.pc + 2
               
                self.pc = self.reg[self.ram[self.pc + 1]]
            
            elif cmd == self.CALL:
                # push return address onto the stack
                self.reg[7] -= 1 # sets stack pointer to 243 in ram
                self.ram[self.reg[7]] = self.pc + 2 # writes 10000010 (line 9, LDI) to call stack at ram index of 243
                self.pc = self.reg[self.ram[self.pc + 1]]
                # print('self pc2', self.pc)
                
            elif cmd == self.RET:
                # POP return address from stack to store in pc
                self.pc = self.ram[self.reg[7]]
                self.reg[7] += 1
                # self.pc += 1


                
            

    # def run_LDI(self):
            
