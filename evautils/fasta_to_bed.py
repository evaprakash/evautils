#!/users/eprakash/anaconda2/bin/python

import sys
import re
from collections import OrderedDict
import argparse

def convert(seqfile, outputfile):
        seqs = OrderedDict()
        fp = open(seqfile, "r")
        print("#Loading " + seqfile + " ...")
        expecting = "label"
        label=''
        for line in fp:
                if expecting == "label":
                        match = re.match(">(.*)$", line)
                        if match:
                                label = match.group(1)
                                expecting = "sequence"
                        else:
                                print("Expecting LABEL but found (!!): " + line)
                                continue
                else:
                        match = re.match("(\w+)$", line)
                        if match:
                                sequence = match.group(1)
                                seqs[label]=sequence
                        else:
                                print("Expecting SEQUENCE but found (!!): " + line)
                        expecting = "label"
                        label=''
        print("#Loaded " + str(len(seqs)) + " sequences")
	fp.close()
	fp=open(outputfile, "w")
	idx=0
	for key in seqs:
		fp.write(key + "\t" + seqs[key]+"\n")
		if idx==len(seqs)-1:
			fp.write(key + "\t" + seqs[key])
		idx=idx+1
	fp.close()

#parser = argparse.ArgumentParser()
#parser.add_argument("sequenceFile", type=str, help="File that contains FASTA sequences")
#parser.add_argument("outputFile", type=str, help="Output file")
#args = parser.parse_args()
#convert(args.sequenceFile, args.outputFile)
