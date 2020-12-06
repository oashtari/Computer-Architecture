# # The index into the memory array, aka location, address, pointer

# # 1 - PRINT_BEEJ
# # 2 - HALT
# # 3 - SAVE_REG store a value in a register
# # 4 - PRINT_REG print the register value in decimal


# memory = [ # think big array of bytes, 8 bits per byte
#     1, # PRINT_BEEJ

#     3, # SAVE_REG R4, 37, instruction itself also called "opcode"       <-- PC
#     4, # 4 and 37 are arguments to SAVE_REG, also called "opreands"
#     37,

#     4, # PRINT_REG R4 # we can use same number again because when PC is at 3, it goes up +3, so it skips that first 4, and after this command, it goes +2, so it skips 3rd 4
#     4, 

#     2 # HALT
# ]

# """
# registers[4] = 37
# """

# registers = [0] * 8

# running = True

# pc = 0  # Program Counter, the index into the memory of the currently-executing instruction

# while running:
#     ir = memory[pc]     # Instruction Register
    
#     if ir == 1:         # PRINT_BEEJ
#         print('Beej!')
#         pc +=1 

#     elif ir == 2:
#         running = False

#     elif ir == 3:       # SAVE_REG
#         reg_num = memory[pc+1]
#         value = memory[pc+2]
#         registers[reg_num] = value
#         # print(f"{registers[reg_num]}") # check to see if value stored
#         pc += 3         # adding 3 because there are 3 different arguments for memory values 3, 4, 37

#     elif ir == 4:       # PRINT_REG
#         reg_num = memory[pc + 1]
#         print(registers[reg_num])
#         pc +=2


# CS 35 code

import sys

#for TESTING
# print(sys.argv) # to pull info out of command line
# sys.exit() # just for testing


"""
Memory
------
Hold bytes

Big array of bytes

To get or set data in memory, you need the index...

These terms are equivalent:
* Index into the memory array
* Address
* Location
* Pointer

"opcode" == the instruction byte
"operands" == arguments to the instruction
"""
PRINT_BEEJ = 1
HALT = 2
SAVE_REG = 3
PRINT_REG = 4
PUSH = 5
POP = 6
CALL = 7
RET = 8


# delete this and make empty memory below with 256 bytes, now we need to load data from a program, see 'with' line below

# memory = [                                  # think big array of bytes, 8 bits per byte
#     1, # PRINT_BEEJ
#     3, # SAVE_REG R1, 37 r[1] = 27          instruction itself also called "opcode"       <-- PC
#     1, # R1                                 
#     37,
#     4, # PRINT_REG R1                       
#     1, # R1
#     1, # PRINT_BEEJ
#     2 # HALT
# ]

memory = [0] * 256


"""
Variables are called 'registers'
* There are a fixed number
* They have preset names: R0, R1, R2, ... R7

Registers can each hold a single byte
"""

register = [0] * 8 # [0,0,0,0,0,0,0,0]

# register[7] = 0xf4 # Stack Pointer

SP = 7
register[SP] = 0xf4


address = 0

if len(sys.argv) != 2:
    print("usage: comp.py progname")
    sys.exit(1)

try:
    with open(sys.argv[1]) as f:  # if file in different directory, would need to put whole path instead of just prog1 // NOW using sys.argv[index] to grab file name
        for line in f:
            line = line.strip() # deletes the extra line when outputting the content of the file

            if line == '' or line[0] == "#":
                continue

            try:
                str_value = line.split("#")[0]
                value = int(str_value)  # can specify a base here, which is necessary for binary --> value = int(str_value, 10) need 2 for binary

            except ValueError:
                print(f"Invalid number: {str_value}")
                sys.exit(1)

            memory[address] = value
            address += 1
except FileNotFoundError:
    print(f"file not found: {sys.argv[1]}")
    sys.exit(2)
# sys.exit(0) # just to end this and not run rest of file

# start execution at address 0


# keep track of the address of the currently executed...
pc = 0 # Program Counter, pointer to the instruction...

halted = False

def push_val(value):
    # decrement the stack pointer
    register[SP] -= 1

    # copy the value onto the stack
    top_of_stack_addr = register[SP]
    memory[top_of_stack_addr] = value

def pop_val():
    # get value from top of stack
    top_of_stack_addr = register[SP]
    value = memory[top_of_stack_addr]

    # increment the SP
    register[SP] += 1

    return value

while not halted:
    instruction = memory[pc]

    if instruction == PRINT_BEEJ:
        print('Beej!')
        pc += 1
    
    elif instruction == HALT:
        halted = True
        pc += 1

    elif instruction == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3

    elif instruction == PRINT_REG:
        reg_num = memory[pc + 1]
        print(register[reg_num])
        pc += 2

    elif instruction == PUSH:
        # decrement the stack pointer
        register[SP] -= 1
        #grab the value out of the given register
        reg_num = memory[pc + 1]
        value = register[reg_num]
        # copy the value onto the stack
        top_of_stack_addr = register[SP]
        memory[top_of_stack_addr] = value

        pc +=2

        # print(memory[0xf0:0xf4])

    elif instruction == POP:
        # get value from top of stack
        top_of_stack_addr = register[SP]
        value = memory[top_of_stack_addr]

        # store in register
        reg_num = memory[pc+1]
        register[reg_num] = value

        #increment stack pointer
        register[SP] += 1

        pc +=2 

    elif instruction == CALL:
        # get address of the next instruction after the CALL
        return_addr = pc + 2

        # push on stack
        push_val(return_addr)

        # get subroutine address from register
        reg_num = memory[pc + 1]
        subroutine_addr = register[reg_num]

        # jump to it
        pc = subroutine_addr

    elif instruction == RET:
        # get return addr from top of stack
        return_addr = pop_val()

        # store it in the pc
        pc = return_addr

    else: 
        print(f"unknonw instruction {instruction} at address {pc}")
        sys.exit(1)


# DAY 2
    # inst_len = ((instruction & 0b11000000) >> 6) + 1
    # inst_len = (instruction & 0b11000000 >> 6) + 1
    # pc += inst_len






# TIM'S SIMPLE MACHINE

# import sys
# ​
# PRINT_TIM = 0b00000001
# HALT      = 0b00000010
# PRINT_NUM = 0b01000011  # a 2-byte command, takes 1 argument
# SAVE      = 0b10000100  # a 3-byte command, takes 2 arguments
# PRINT_REG = 0b01000101
# ADD       = 0b10100110 
# ​
# ​
# # a data-driven machine
# # function call
# # a "variable" == registers for our programs to save things into
# ​
# ​
# # RAM
# memory = [0] * 256
# ​
# # registers, R0-R7
# registers = [0] * 8
# ​
# running = True
# ​
# # program counter
# pc = 0
# ​
# def load_ram():
#     try:
#         if len(sys.argv) < 2:
#             print(f'Error from {sys.argv[0]}: missing filename argument')
#             print(f'Usage: python3 {sys.argv[0]} <somefilename>')
#             sys.exit(1)
# ​
# ​
#         # add a counter that adds to memory at that index
#         ram_index = 0
# ​
#         with open(sys.argv[1]) as f:
#            for line in f:
#                 split_line = line.split("#")[0]
#                 stripped_split_line = split_line.strip()
# ​
#                 if stripped_split_line != "":
#                     command = int(stripped_split_line, 2)
                    
#                     # load command into memory
#                     memory[ram_index] = command
# ​
#                     ram_index += 1
# ​
#     except FileNotFoundError:
#         print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
#         print("(Did you double check the file name?)")
# ​
# load_ram()
# ​
# while running:
#     command = memory[pc]
# ​
# ​
#     if command == PRINT_TIM:
#         print('tim!')
# ​
#     elif command == PRINT_NUM:
#         num_to_print = memory[pc + 1]  # we already incremented PC!
#         print(num_to_print)
# ​
#         # pc += 1   # but increment again
# ​
# ​
#     elif command == SAVE:
#         num_to_save = memory[pc + 1]
#         register_address = memory[pc + 2]
# ​
#         registers[register_address] = num_to_save
# ​
#         # shorter: 
#         # registers[memory + 2] = memory[pc + 1]
# ​
#         # pc += 2
# ​
#     elif command == PRINT_REG:
#         reg_address = memory[pc + 1]
# ​
#         saved_number = registers[reg_address]
# ​
#         print(saved_number)
# ​
#         # print(registers[memory[pc + 1]])
# ​
#     elif command == ADD:
#         reg1_address = memory[pc + 1]
#         reg2_address = memory[pc + 2]
# ​
#         registers[reg1_address] += registers[reg2_address]
# ​
#     elif command == HALT:
#         running = False
# ​
#     number_of_operands = command >> 6
#     pc += (1 + number_of_operands)
#     # pc += 1  # so we don't get sucked into an infinite loop!


# PROGRAM CODE 
# 00000001  # print tim
# 00000001  # print tim
# 01000011  # print num
# 00101010  # the number 42
# 10000100 # save
# 01100011  # 99
# 00000010  # into R2
# 10000100 # save
# 00000001 # the number 1
# 00000011 # into R3
# 10100110 # ADD (R2 += R3)       <-- PC
# 00000010 # R2
# 00000011 # R3
# 01000101  # print reg
# 00000010  # R2 again - should be 100 now! 
# 00000010  # but this time it's the command halt