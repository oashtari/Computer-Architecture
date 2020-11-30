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

halted = False

# keep track of the address of the currently executed...
pc = 0 # Program Counter, pointer to the instruction...

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

    else: 
        print(f"unknonw instruction {instruction}")
        sys.exit(1)

# DAY 2
    # inst_len = ((instruction & 0b11000000) >> 6) + 1
    # inst_len = (instruction & 0b11000000 >> 6) + 1
    # pc += inst_len