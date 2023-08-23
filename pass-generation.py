#!/usr/bin/env python
'''Script to emulate the 192-bit password generation of Lockbit 3.0'''

import sys

# Bit manipulation functions derived from the code at
# https://www.geeksforgeeks.org/rotate-bits-of-an-integer/

TOTAL_BITS = 32

def rotate_left(value, shift):
    '''Rotate left the value d bits'''
    return ((value << shift) | (value >> (TOTAL_BITS - shift))) & 0x00FFFFFFFF

def rotate_right(value, shift):
    '''Rotate right the value d bits'''
    return (value >> shift) | (value << (TOTAL_BITS - shift)) & 0x00FFFFFFFF

def bit_negate(value):
    '''Negate the bits of value'''
    return 0x00FFFFFFFF ^ value

def bit_rotate(value):
    '''Perform a bit rotation of value'''
    return (((value << 24) & 0xFF000000) |
            ((value <<  8) & 0x00FF0000) |
            ((value >>  8) & 0x0000FF00) |
            ((value >> 24) & 0x000000FF))


SECRET_KEY = "db66023ab2abcb9957fb01ed50cdfa6a" if len(sys.argv) < 2 else sys.argv[1]

BLOCKS = [bit_rotate(int(SECRET_KEY[i:i+8], 16)) for i in range(0, 32, 8)]
FINAL_OUTPUT = []

for ITER in range(6):
    TEMP_LIST = []
    REG_A = BLOCKS[0]
    REG_A = bit_rotate(REG_A)
    REG_A = rotate_right(REG_A, 0x0d)
    REG_B = bit_negate(REG_A)

    REG_A = BLOCKS[1]
    REG_A = rotate_left(REG_A, 0xb)
    REG_A = bit_rotate(REG_A)
    TEMP_LIST.append(bit_rotate(REG_A ^ REG_B))

    REG_A = BLOCKS[2]
    REG_A = rotate_left(REG_A, 0x9)
    REG_A = bit_rotate(REG_A)
    REG_B = REG_A
    REG_B = bit_negate(REG_B)
    TEMP_LIST.append(bit_rotate(REG_A))

    REG_A = BLOCKS[3]
    REG_A = rotate_left(REG_A, 0x7)
    REG_A = bit_rotate(REG_A)
    REG_A = REG_A ^ REG_B
    REG_B = bit_negate(REG_A)
    TEMP_LIST.append(bit_rotate(REG_A))

    REG_A = rotate_left(REG_A, 0x5)
    REG_A = REG_A ^ REG_B
    TEMP_LIST.append(bit_rotate(REG_A))

    FINAL_OUTPUT += TEMP_LIST

    for index in range(4):
        BLOCKS[index] = bit_rotate(TEMP_LIST[index])

for word in FINAL_OUTPUT:
    print("%08x" % word)
