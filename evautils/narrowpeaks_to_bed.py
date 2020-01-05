#!/users/eprakash/anaconda2/bin/python

import sys
import re
from collections import OrderedDict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("regionSize", type=int,
                    help="Size of region in base pairs e.g. 400")
args = parser.parse_args()
regionSize = args.regionSize
#print("regionSize is " + str(regionSize))


for line in sys.stdin:
	match = re.match("(\S+)\s+(\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\d+)\s*$", line)
	if match:
		chrom = match.group(1)	
		chromStart = int(match.group(2))
		chromSummitOffset = int(match.group(3))
		regionStart = chromStart + chromSummitOffset - int(regionSize/2)
		regionEnd = regionStart + regionSize
		print("" + chrom + "\t" + str(regionStart) + "\t" + str(regionEnd))
