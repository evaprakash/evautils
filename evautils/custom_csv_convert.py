#!/users/eprakash/anaconda2/bin/python

import sys


if len(sys.argv) < 2:
        print("Usage: {} filename".format(sys.argv[0]))
        exit(1)

fname = sys.argv[1]
fp = open(fname, "r")
for line in fp:
	(motif, rest) = line.split(": ")
	(auroc, auprc, hits) = rest[1:-2].split(", ")
	print str(motif) + ", "  + str(auroc) + ", " + str(auprc) +  ", " + str(hits)
fp.close()




