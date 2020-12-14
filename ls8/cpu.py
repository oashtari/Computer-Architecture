"""CPU functionality."""

import sys
import time 

class CPU:
    """Main CPU class."""
    
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[7] = 0xF4
        self.pc_jump = 0
        self.fl = 0b000
        self.commands = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100000: self.add,
            0b10100001: self.sub,
            0b10100010: self.mul,
            0b10100011: self.div,
            0b01000101: self.push,
            0b01000110: self.pop, 
            0b01010000: self.call,
            0b00010001: self.ret, 
            0b10100111: self.cmp,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            # 0b10101000: self.band,
            # 0b10101010: self.bor, 
            # 0b10101011: self.bxor, 
            # 0b01101001: self.bnot, 
            # 0b10101100: self.shl,
            # 0b10101101: self.shr, 
            # 0b10100100: self.mod,
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
                print('an error:', error)
            # print('THE PROGRAM', self.ram[13])
        
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


    def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

        elif op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]

        elif op == "BAND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]

        elif op == "BOR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]

        elif op == "BXOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]

        elif op == "BNOT":
            self.reg[reg_a] = ~self.reg[reg_a] 

        elif op == "SHL":
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]

        elif op == "SHR":
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]

        else:
            raise Exception('this ALU not supported')

        # reg_a = self.reg[self.ram_read(self.pc+1)] 
        # reg_b = self.reg[self.ram_read(self.pc+2)]

        # def add():
        #     self.reg[reg_a] += self.reg[reg_b]

        # def sub():
        #     self.reg[reg_a] -= self.reg[reg_b]

        # def mul():
        #     reg_a *= reg_b

        # def div():
        #     self.reg[reg_a] /= self.reg[reg_b]
        
        # def mod():
        #     self.reg[reg_a] %= self.reg[reg_b]

        # def inc():
        #     self.reg[reg_a] += 1

        # def dec():
        #     self.reg[reg_a] -= 1

        # def band():
        #     self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]

        # def bor():
        #     self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]

        # def bxor():
        #     self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]

        # def bnot():
        #     self.reg[reg_a] = ~self.reg[reg_a] 

        # def shl():
        #     self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]

        # def shr():
        #     self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]

        # operations = {
        #     0b10100000: add,
        #     0b10100001: sub,
        #     0b10100010: mul,
        #     0b10100011: div,
        #     0b01000101: push,
        #     0b01000110: pop, 
        #     0b01010000: call,
        #     0b00010001: ret, 
        #     0b10100111: cmp,
        #     0b01010100: jmp,
        #     0b01010101: jeq,
        #     0b01010110: jne,
        #     0b10101000: band,
        #     0b10101010: bor, 
        #     0b10101011: bxor, 
        #     0b01101001: bnot, 
        #     0b10101100: shl,
        #     0b10101101: shr, 
        #     0b10100100: mod,
        #     0b01100101: inc,
        #     0b01100110: dec,
        # }


        # try: 
        #     operations[op]
        # # else:
        # #     raise Exception("Unsupported ALU operation")
        # except KeyError:
        #     print("Unsupported ALU operation")

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

        # print('TRACE WHAT')

    def ldi(self):
            self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
            self.pc += 3

    def prn(self):
            print('print itself:', self.reg[self.ram_read(self.pc+1)])
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

    def call(self):
        return_addr = self.pc + 2

        self.reg[7] -= 1

        top_of_stack_addr = self.reg[7]
        self.ram[top_of_stack_addr] = return_addr

        reg_num = self.ram[self.pc + 1]
        subroutine_addr = self.reg[reg_num]

        self.pc = subroutine_addr 

    def ret(self):
        top_of_stack_addr = self.reg[7]
        value = self.ram[top_of_stack_addr]

        self.reg[7] += 1

        return_addr = value

        self.pc = return_addr

    def cmp(self):
        reg_a = self.reg[self.ram_read(self.pc+1)] 
        reg_b = self.reg[self.ram_read(self.pc+2)]
        
        if reg_a < reg_b:
            self.fl = 0b00000100
        elif reg_a > reg_b:
            self.fl = 0b00000010
        else:
            self.fl = 0b00000001
        self.pc +=3

    def jmp(self):
        go_to = self.reg[self.ram_read(self.pc + 1)]

        self.pc = go_to
    
    def jeq(self):
        if self.fl == 0b001:
            self.jmp()
        else:
            self.pc +=2

    def jne(self):
        if self.fl > 1 or self.fl == 0b000: #  self.fl >1 or 
            self.jmp()
        else: 
            self.pc +=2

    def jge(self):
        pass

    def jgt(self):
        pass

    def jle(self):
        pass

    def jlt(self):
        pass

    def add(self):
        self.aluRun('ADD')

    def sub(self):
        self.aluRun('SUB')

    def mul(self):
        self.aluRun('MUL')
        # reg_a = self.reg[self.ram_read(self.pc+1)] 
        # reg_b = self.reg[self.ram_read(self.pc+2)]
        # reg_a *= reg_b
        # self.alu('MUL', reg_a, reg_b)

    def div(self):
        self.aluRun('DIV')
    
    # def mod(self):
    #     self.aluRun('MOD')

    # def band(self):
    #     self.aluRun('BAND')

    # def bor(self):
    #     self.aluRun('BOR')

    # def bxor(self):
    #     self.aluRun('BXOR')

    # def bnot(self):
    #     self.aluRun('BNOT')

    # def shl(self):
    #     self.aluRun('SHL')

    # def shr(self):
    #     self.aluRun('SHR')
    
    def aluRun(self, action):
        self.alu(action, self.ram_read(self.pc+1), self.ram_read(self.pc+2))
        self.pc +=3

    def run(self):
        """Run the CPU."""
        ldi = 0b10000010
        prn = 0b01000111
        hlt = 0b00000001
        mul = 0b10100010
        push = 0b01000101
        pop = 0b01000110

        # self.load()

        # halt = False

        # while halt is not True:
        while self.ram_read(self.pc) != 0b00000001:
            instruction = self.ram_read(self.pc)
            # print('run inst', instruction)
            # print('intitial instruction', instruction)
            # print('inst pc spot', self.pc)
            # print('pointer', self.reg[7])

            # try: 
            self.commands[instruction]()
                # print('pointer moved?', self.reg[7])

            # except Exception:
            #     return print(f'Instruction {instruction} not found at {self.pc}')

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
