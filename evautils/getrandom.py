#!/usr/bin/python

import sys
import os
import random

if len(sys.argv) < 3:
	print("Usage: {} filename number_of_sequences_to_randomly_extract".format(sys.argv[0]))
	exit(1)

filename = sys.argv[1]
number = int(sys.argv[2])
numlines = int(os.popen("wc -l {} | cut -d ' ' -f 1".format(filename)).read())/2
linenums = random.sample(range(0, numlines), number)
linenums.sort()
fp = open(filename, "r")
array_position=0
current_line=0
skip_next = False
print_next = False
should_exit = False
for line in fp:
	if skip_next:
		if print_next:
			print(line.strip("\n"))
		skip_next = False
		if should_exit:
			fp.close()
			exit(0)
	else:
		if (linenums[array_position] == current_line):
			print(line.strip("\n"))
			array_position=array_position+1
			skip_next = True
			print_next = True
			if (array_position >= len(linenums)):
				should_exit = True
		else:
			skip_next = True
			print_next = False
		current_line = current_line+1
fp.close()

