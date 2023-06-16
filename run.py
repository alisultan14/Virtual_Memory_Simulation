#! /usr/bin/env python

from __future__ import print_function
import sys
from optparse import OptionParser
import random
import math


def mustbepowerof2(bits, size, msg):
    if math.pow(2,bits) != size:
        print('Error in argument: %s' % msg)
        sys.exit(1)

def mustbemultipleof(bignum, num, msg):
    if (int(float(bignum)/float(num)) != (int(bignum) / int(num))):
        print('Error in argument: %s' % msg)
        sys.exit(1)
        

def check_machine_word_multiple_of_8(word):
    if word % 8 != 0:
        print("Error: machine word must be a multiple of 8.")
        sys.exit(1)

def PTE_valid_check(pa_bits, control_bits, word):
    if pa_bits + control_bits >= word:
        print("Error: The sum of PFN bits and control bits must be less than or equal to the machine word.")
        sys.exit(1)

def decimal_to_binary(decimal_number,word_size):
    binary_number = bin(decimal_number)[2:] # Convert decimal to binary without the '0b' prefix
    padded_binary_number = binary_number.zfill(word_size) # Pad with zeros to make it the specified word size
    return padded_binary_number

def binary_to_hex(binary_string):
    decimal_number = int(binary_string, 2) # Convert binary string to decimal
    hex_number = hex(decimal_number)[2:] # Convert decimal to hexadecimal without the '0x' prefix
    return hex_number

def binary_to_decimal(binary_string):
    decimal_number = 0
    for digit in binary_string:
        decimal_number = decimal_number * 2 + int(digit)
    return decimal_number






def convert(size):
    length = len(size)
    lastchar = size[length-1]
    if (lastchar == 'k') or (lastchar == 'K'):
        m = 1024
        nsize = int(size[0:length-1]) * m
    elif (lastchar == 'm') or (lastchar == 'M'):
        m = 1024*1024
        nsize = int(size[0:length-1]) * m
    elif (lastchar == 'g') or (lastchar == 'G'):
        m = 1024*1024*1024
        nsize = int(size[0:length-1]) * m
    else:
        nsize = int(size)
    return nsize

#Parse command-line arguments and set simulation parameters.
parser = OptionParser()
parser.add_option('-A', '--addresses', default='-1',
                  help='a set of comma-separated pages to access; -1 means randomly generate', 
                  action='store', type='string', dest='addresses')
parser.add_option('-s', '--seed',    default=0,     help='the random seed',                               action='store', type='int', dest='seed')
parser.add_option('-v', '--asize',   default='16k', help='address space size (e.g., 16, 64k, 32m, 1g)',   action='store', type='string', dest='asize')
parser.add_option('-p', '--physmem', default='64k', help='physical memory size (e.g., 16, 64k, 32m, 1g)', action='store', type='string', dest='psize')
parser.add_option('-f', '--pagesize', default='4k', help='page size (e.g., 4k, 8k, whatever)',            action='store', type='string', dest='pagesize')
parser.add_option('-n', '--numaddrs',  default=5,  help='number of virtual addresses to generate',       action='store', type='int', dest='num')
parser.add_option('-u', '--used',       default=50, help='percent of virtual address space that is used', action='store', type='int', dest='used')
parser.add_option('-e',                             help='verbose mode',                                  action='store_true', default=False, dest='verbose')
parser.add_option('-w', '--word_size',default = 32,                       help='machine word',                                  action='store', type='int', dest='word')
parser.add_option('-c',                             help='compute answers for me',                        action='store_true', default=False, dest='solve')
parser.add_option('-b', '--control_bits',default = 1,                       help='control bits to be used in the PTE',                                  action='store', type='int', dest='control_bits')

#Calculate basic information about the page table, such as the number of virtual and physical pages, the number of bits needed to represent virtual and physical addresses, and the size of the page table.

(options, args) = parser.parse_args()

print("This is the information you provided:")
print('')
print('ARG seed:', options.seed)
print('ARG address space size:', options.asize)
print('ARG phys mem size:', options.psize)
print('ARG page size:', options.pagesize)
print('ARG number of addrs:', options.num)
print('ARG percent used:', options.used)
print('ARG verbose:', options.verbose)
print('ARG machine word:', options.word)
print('ARG compute answers:', options.solve)
print('ARG control_bits:', options.control_bits)
print('')
random.seed(options.seed)

asize    = convert(options.asize)
psize    = convert(options.psize)
pagesize = convert(options.pagesize)
word_size = int(options.word)
control_bits = int(options.control_bits)
addresses = str(options.addresses)

#Check for errors in the given parameters and exit the program if any are found.

if psize <= 1:
    print('Error: must specify a non-zero physical memory size.')
    exit(1)

if asize < 1:
    print('Error: must specify a non-zero address-space size.')
    exit(1)

if psize <= asize:
    print('Error: physical memory size must be GREATER than address space size (for this simulation)')
    exit(1)

# if psize >= convert('1g') or asize >= convert('1g'):
#     print('Error: must use smaller sizes (less than 1 GB) for this simulation.')
#     exit(1)

if control_bits >= word_size:
    print('Error: control bits must be less than the machine word so that there is space for PFN bits')
    exit(1)

if control_bits == 0:
    print('Error: control bits cannot be 0 as one bit has to be used as the valid bit')
    exit(1)


mustbemultipleof(asize, pagesize, 'address space must be a multiple of the pagesize')
mustbemultipleof(psize, pagesize, 'physical memory must be a multiple of the pagesize')
check_machine_word_multiple_of_8(word_size)

#Initialize arrays to keep track of the used physical pages and the page table entries.

#page table basic_info
page_table_info = {}
page_table_info["virtual_pages"] = int(asize / pagesize)
page_table_info["va_bits"] = int(math.log(float(asize))/math.log(2.0))
page_table_info["vpn_bits"] = int(math.log(float(page_table_info["virtual_pages"]))/math.log(2.0))
page_table_info["physical_pages"] = int(psize/pagesize)
page_table_info["pa_bits"] = int(math.log(float(psize))/math.log(2.0))
page_table_info["pfn_bits"] = int(math.log(float(page_table_info["physical_pages"]))/math.log(2.0))
PTE_valid_check(page_table_info["pfn_bits"], control_bits,word_size)
page_table_info["pt_size"] = int((word_size/8) * page_table_info["virtual_pages"])
page_table_info["pt_pages"] = int(page_table_info["pt_size"] / pagesize)


#using arrays to keep track of the page table and also the pages which are valid
import array
used = array.array('i')
pt   = array.array('i')
for i in range(0,page_table_info["physical_pages"]):
    used.insert(i,0)

#Generate the page table by randomly assigning physical frames to virtual pages based on the specified percentage of used virtual address space.

print("Question 1: Given the information above, answer the following questions about the Page Table:")
print("")
print("What is the Virtual Memory Page Count?")
if (options.solve):
    print("Answer: " + str(page_table_info['virtual_pages']))
print("What is the Physical Memory Frame Count? ")
if (options.solve):
    print("Answer: " + str(page_table_info['physical_pages']))
print("What is the PTE organisation?")
if (options.solve):
    print("Answer: PTE organisation is equal to word size: {} bits which is composed of (PFN: {} bits) + (Control Bits: {} bits) + (Leftover Bits: {})".format(str(options.word), str(page_table_info['pfn_bits']), str(control_bits), str(options.word - page_table_info["pfn_bits"] - control_bits)))
print("What is the Page Table Size?")
if (options.solve):
    print("Answer: " + str(page_table_info['pt_size'])+ " bytes")
print("How many pages are there in the Page Table")
if (options.solve):
    print("Answer: " + str(page_table_info['pt_pages'])+ " pages")

print(" ")
print("Question 2: Draw out the Page Table. ")
for v in range(0,page_table_info['virtual_pages']):
    done = 0
    while done == 0:
        if ((random.random() * 100.0) > (100.0 - float(options.used))):
            u = int(page_table_info['physical_pages'] * random.random())
            if used[u] == 0:
                used[u] = 1
                done = 1
                if (options.solve):
                    print('  [%20d]  ' % v, end='')
                    entry_binary = '1' + decimal_to_binary(u,word_size)[1:]
                    entry_hex = binary_to_hex(entry_binary)
                    print("0x"+entry_hex)
                pt.insert(v,u)
        else:
            if (options.solve):
                    print('  [%20d]  ' % v, end='')

                    print("0x"+"0"*int(word_size/4))
            pt.insert(v,-1)
            done = 1
print(''    )


addrList = []

# Generate a list of virtual addresses to translate, either by randomly generating them or by using a user-specified list.
for i in range(0, options.num):
    n = int(asize * random.random())
    if n not in addrList: 
        addrList.append(n)
    else:
        addrList = addresses.split(',')

    

#Translate the virtual addresses to physical addresses by looking up the corresponding page table entries and calculating the physical frame numbers.

print('Question 3: Translate the following Virtual Addresses to the Physical Addresses they map to')
print("")
for vStr in addrList:
    # vaddr = int(asize * random.random())
    vaddr = int(vStr)
    vaddr_binary = decimal_to_binary(vaddr,page_table_info['va_bits'])
    vaddr_hex = binary_to_hex(vaddr_binary)
    print(' VA 0x' + vaddr_binary+ ": Is this Virtual Address valid (in Physical Memory) or Not. What is the PFN that it translates to?")
    if (options.solve):
        print("Answer:")
        vpn_bits_string = vaddr_binary[:page_table_info['vpn_bits']]
        off_set_bits = vaddr_binary[page_table_info['vpn_bits']:]

        vpn_decimal = binary_to_decimal(vpn_bits_string)
        print("Vpn #")
        print(vpn_decimal)
        physical_page_number = pt[vpn_decimal]
        if (physical_page_number < 0):
            print("The address is not in Physical Memory")
        else:
            pfn_bits = decimal_to_binary(pt[v],page_table_info['pfn_bits'])     
            physical_address = pfn_bits + off_set_bits
            print("The Physical Address it translates to: ")
            print(physical_address)
    print(" ")
    




















