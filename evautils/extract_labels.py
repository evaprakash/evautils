#!/usr/bin/python

import sys
import re

if len(sys.argv) < 2:
	print("Usage: {} filename".format(sys.argv[0]))
	exit(1)

filename = sys.argv[1]
fp = open(filename, "r")
for line in fp:
	match = re.match("([^\s]+)\s+\d+$", line)
	if match:
		label = match.group(1)
		print(label)
	else:
		continue
fp.close()

