#!/users/eprakash/anaconda2/bin/python

import sys


if len(sys.argv) < 3:
        print("Usage: {} two filenames".format(sys.argv[0]))
        exit(1)

fname_order_by = sys.argv[1]
fname = sys.argv[2]
fp = open(fname, "r")
fp_order_by = open(fname_order_by, "r")
fp_index=0
fp_order_by_list=[]
for line in fp_order_by:
	motif = line.split(",")[0]
	fp_order_by_list.append(motif)
for line in fp:
	motif = line.split(",")[0]
	if motif not in fp_order_by_list:
		print("?")
	else:
		print((fp_order_by_list.index(motif)+1))
fp.close()
fp_order_by.close()
