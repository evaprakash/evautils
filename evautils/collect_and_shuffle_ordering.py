#!/users/eprakash/anaconda2/bin/python

import sys
import re
from collections import OrderedDict
import argparse
import random


def load_sequences(seqfile, num=-1):
	seqs = OrderedDict()
	fp = open(seqfile, "r")
	print("#Loading " + seqfile + " ...")
	expecting = "label"
	label=''
	numSeen = 0
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
				numSeen = numSeen+1
			else:
				print("Expecting SEQUENCE but found (!!): " + line)
			expecting = "label"
			label=''
		if num != -1 and numSeen >= num:
			break
	fp.close()
	print("#Loaded " + str(len(seqs.keys())) + " sequences from " + seqfile)
	return seqs

parser = argparse.ArgumentParser()
parser.add_argument("positiveSequenceFile", type=str,
                    help="File that contains positive (for training set)  FASTA sequences")
parser.add_argument("positiveNumber", type=int,
                    help="Number of positive sequences to take (-1 for all)")
parser.add_argument("negativeSequenceFile", type=str,
                    help="File that contains negative (for training set)  FASTA sequences")
parser.add_argument("negativeNumber", type=int,
                    help="Number of negative sequences to take (-1 for all)")
parser.add_argument("saveLabelsToFile", type=str,
                    help="file name to sequence labels (marked as 1 or 0 for positive or negative)")

args = parser.parse_args()
seqs = OrderedDict()
positiveSeqs = load_sequences(args.positiveSequenceFile, args.positiveNumber)
negativeSeqs = load_sequences(args.negativeSequenceFile, args.negativeNumber)
positiveSet = set(positiveSeqs.keys())
negativeSet = set(negativeSeqs.keys())
commonToBothSets = positiveSet.intersection(negativeSet)
print("There are %s labels common to both positive and negative set, will be removed" % str(len(commonToBothSets)))

for seqLabel in commonToBothSets:
	del positiveSeqs[seqLabel]
	del negativeSeqs[seqLabel]
	
seqs.update(positiveSeqs)
seqs.update(negativeSeqs)

total = len(seqs)
print("Got a total of " + str(total) + " sequences")

seqsAsList = seqs.items()
order = random.sample(range(total), total)
labelsFile = open(args.saveLabelsToFile, "w")

for i in order:
	item = seqsAsList[i]
	print(">" + item[0])
	print(item[1])
	if item[0] in positiveSet:
		labelsFile.write("%s\t1\n" % item[0])
	else:
		labelsFile.write("%s\t0\n" % item[0])
labelsFile.close()
