The program simulates a virtual memory system and performs various operations, such as generating a page table, translating virtual addresses to physical addresses, and answering questions about the page table.

Overview of the Program

The program simulates a virtual memory system by:

Parsing command-line arguments and setting simulation parameters.
Calculating basic information about the page table, such as the number of virtual and physical pages, the number of bits needed to represent virtual and physical addresses, and the size of the page table.
Checking for errors in the given parameters and exiting the program if any are found.
Initializing arrays to keep track of the used physical pages and the page table entries.
Generating the page table by randomly assigning physical frames to virtual pages based on the specified percentage of used virtual address space.
Translating the virtual addresses to physical addresses by looking up the corresponding page table entries and calculating the physical frame numbers.
Input Parameters

The following command-line options are available:

-A, --addresses: a set of comma-separated pages to access; -1 means randomly generate (default: -1)
-s, --seed: the random seed (default: 0)
-v, --asize: address space size (e.g., 16, 64k, 32m, 1g) (default: '16k')
-p, --physmem: physical memory size (e.g., 16, 64k, 32m, 1g) (default: '64k')
-f, --pagesize: page size (e.g., 4k, 8k, whatever) (default: '4k')
-n, --numaddrs: number of virtual addresses to generate (default: 5)
-u, --used: percent of virtual address space that is used (default: 50)
-e: verbose mode (default: False)
-w, --word_size: machine word (default: 32)
-c: compute answers for me (default: False)
-b, --control_bits: control bits to be used in the PTE (default: 1)
Output

The program will output the following information:

This Python program simulates a basic page table for a given address space, physical memory, and page size, while taking into account the machine word size and the number of control bits used in the page table entries (PTEs). The program consists of three main questions that can be answered by activating the -c option. The questions are as follows:

(1) The first question asks for the virtual memory page count, physical memory frame count, PTE organization, page table size, and the number of pages in the page table.

(2) The second question asks the user to draw out the page table based on the given information. When the -c option is activated, the program will display the generated page table entries with their corresponding virtual page numbers (VPNs) and physical frame numbers (PFNs). The PTEs are the word size and are printed out in Hexadecimal for this simulation

(3) The third question asks the user to translate a set of given virtual addresses to their corresponding physical addresses. When the -c option is activated, the program will perform the translations and display the resulting physical addresses along with whether the virtual addresses are valid in the physical memory or not.

By activating the -c option, the program will provide the correct answers to these questions, allowing users to gain a better understanding of the page table simulation and how different parameters affect the overall virtual-to-physical address translation process.

There are several restrictions and assumptions made in this program:

(1) The PTE size is equal to the specified machine word size, which must be a multiple of 8.
(2) There must be at least one control bit in the PTE.
(3) The physical memory size must be larger than the virtual memory size for this simulation.
(4) Both the physical memory size and the virtual memory size must be multiples of the page size.
(5) The program only accepts sizes with 'K', 'M', or 'G' prefixes, and these sizes must be powers of two for consistency.
(6) The page table, when printed out as the answer to question 2, is displayed in hexadecimal format.


How to Run the Program:

To run the program, use the following command format in your terminal:
python <Project-2.py> [options]

Example usage:
python virtual_memory_simulation.py -A -1 -s 0 -v 16k -p 64k -f 4k -n 5 -u 50 -w 32 -c

Note:
The program is designed for educational purposes to help users understand the basic concepts and operations of virtual memory systems.
