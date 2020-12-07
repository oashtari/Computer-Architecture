"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xF4
        self.pc_jump = 0
        self.commands = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100000: self.add,
            0b10100001: self.sub,
            0b10100010: self.mul,
            0b10100011: self.div,
            0b01000101: self.push,
            0b01000110: self.pop
        }



    def load(self):
        """Load a program into memory."""

        address = 0
        # OLD CODE
        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        program = []

        if len(sys.argv) == 2:
            try:
                with open(sys.argv[1]) as f:
                    print('loaded', sys.argv[1])
                    for line in f:
                        line = line.strip()

                        if line == '' or line[0] == '#':
                            # print('will it continue')
                            continue

                        try:
                            str_value = line.split('#')[0]
                            self.ram[address] = int(str_value,2)
                            address +=1

                        except ValueError:
                            print(f'Invalid number: {str_value}')
                

            except FileNotFoundError as error:
                print(error)
            print('THE PROGRAM', self.ram[13])
        
            # for instruction in program:
            #     print('ram instruction', instruction)
            #     self.ram[address] = instruction
            #     address += 1

        else:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            print("(Did you double check the file name?)")



    def ram_read(self, memory_address_register):
        return self.ram[memory_address_register]

    def ram_write(self, memory_address_register, memory_data_register):
        self.ram[memory_address_register] = memory_data_register


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

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

    def ldi(self):
            self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
            self.pc += 3

    def prn(self):
            print(self.reg[self.ram_read(self.pc+1)])
            self.pc += 2

    def push(self, address = None):
        self.reg[7] -= 1

        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]

        top_of_stack_addr = self.reg[7]
        self.ram[top_of_stack_addr] = value 

        self.pc +=2
        # if address is None:
        #     self.reg[7] -= 1
        #     self.ram_write(self.reg[7], self.reg[self.ram_read(self.pc+1)])
        # else:
        #     self.reg[7] -= 1
        #     self.ram_write(self.reg[7], address)

    def pop(self):

        top_of_stack_addr = self.reg[7]
        # print('top of', top_of_stack_addr)
        value = self.ram[top_of_stack_addr]
        # print('value from ram', value)
        # print('anything')

        reg_num = self.ram[self.pc+1]
        # print('reg num', reg_num)
        self.reg[reg_num] = value
        # print('assignment', self.reg[reg_num])

        # print('pre pointer', self.reg[7])
        self.reg[7] += 1
        # print('post pointer', self.reg[7])

        self.pc += 2
        # if self.reg[7] == 0xF4:
        #     return print('Stack is empty.')
        # if ret:
        #     pc = self.ram_read(self.reg[7])
        #     self.reg[7] += 1
        #     return pc
        # self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.reg[7])
        # self.reg[7] += 1

    def add(self):
        self.aluRun('ADD')

    def sub(self):
        self.aluRun('SUB')

    def mul(self):
        self.aluRun('MUL')

    def div(self):
        self.aluRun('DIV')

    def aluRun(self, action):
        self.alu(action, self.ram_read(self.pc+1), self.ram_read(self.pc+2))
        self.pc +=3

    def run(self):
        """Run the CPU."""
        # ldi = 0b10000010
        # prn = 0b01000111
        # hlt = 0b00000001
        # mul = 0b10100010
        # push = 0b01000101
        # pop = 0b01000110

        # self.load()

        halt = False

        # while halt is not True:
        while self.ram_read(self.pc) != 0b00000001:
            instruction = self.ram_read(self.pc)
            # print('intitial instruction', instruction)
            # print('inst pc spot', self.pc)
            # print('pointer', self.reg[7])

            try: 
                self.commands[instruction]()
                # print('pointer moved?', self.reg[7])

            except Exception:
                return print(f'Instruction {instruction} not found at {self.pc}')

            # if instruction == hlt or self.pc > 10:
            #     halt = True
            #     # print('HLT')
            
            # elif instruction == ldi:
            #     # print('LDI')
            #     # self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
            #     # self.pc += 3

            # elif instruction == prn:
            #     # print('PRN')
            #     # print(self.reg[self.ram_read(self.pc+1)])
            #     # self.pc += 2

            # elif instruction == mul:
            #     # print('MUL')
            #     # self.alu('MUL', self.ram_read(self.pc+1), self.ram_read(self.pc+2))
            #     # self.pc += 3
