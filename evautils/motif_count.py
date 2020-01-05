#!/users/eprakash/anaconda2/bin/python
import re
import numpy as np
import argparse
import sys
import operator
from collections import OrderedDict

def count(motif_matches_file, count_option, output_file):
        fp=open(motif_matches_file,'r')
        motifs=OrderedDict()
	motif_list=[]
	linecount=0
        for line in fp:
		if (linecount % 100000 == 0):
			print ("Processing line " + str(linecount))
                match=re.match("((\w|\-)+)\s+((\w|\:|\-)+)\s+(\d+)\s+(\d+)\s+(\+|\-)\s+.+\s+(\w+)$", line)
		motif=re.match("(\d+\-(\w+)\-\d+)",match.group(1)).group(2)
                if (count_option=='hits'):
			if (motif not in motifs):
				motifs.update({motif:1})
			else:
				motifs[motif]=motifs[motif]+1
		else if (count_option=="seqs"):
			sequence=match.group(3)
			if (motif not in motifs):
                                motifs.update({motif:{sequence}})
                        else:
				if (sequence not in motifs[motif]):
                                	motifs[motif].add(sequence)
		else:
			motif_list.append(motif)
		linecount = linecount+1
        fp.close()
	fp=open(output_file, 'w')
	if (count_option=='hits'):
		motif_list=sorted(motifs, key=lambda x: motifs[x])[::-1]
	else if (count_option=='seqs'):
		motif_list=sorted(motifs, key=lambda x: len(motifs[x]))[::-1]
	else:
		motif_list=set(motif_list)
	if (count_option=='hits' or count_option=='seqs'):
		for motif in motif_list:
			if (count_option=='hits'):
				fp.write(motif+"\t"+str(motifs[motif])+"\n")
			else:
				fp.write(motif+"\t"+str(len(motifs[motif]))+"\n")
	else:
		fp.write(motif_list)
	fp.close()

parser = argparse.ArgumentParser()
parser.add_argument("motifMatchesFile", type=str, help="File that contains motif matches, generated from scanmotifgenomewide")
parser.add_argument("countOption", type=str, help="Either 'hits' or 'seqs' or 'dictionary'")
parser.add_argument("outputFile", type=str, help="Output file")
args = parser.parse_args()
count(args.motifMatchesFile, args.countOption, args.outputFile)
