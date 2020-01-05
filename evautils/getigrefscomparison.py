#!/usr/bin/python

from collections import OrderedDict
import sys
import re


def getMotif2AuprcDict(filename):
	fp = open(filename, "r")
	motifdict = OrderedDict()
	for line in fp:
		match = re.match("(\w+):\s+\[(.+),\s+(.+),\s+(.+)\]", line)
		if match:
			motif = match.group(1)
			auroc = float(match.group(2))
			auprc = float(match.group(3))
			unknown = float(match.group(4))
			motifdict[motif] = auprc
	fp.close()
	return motifdict

def mySort(mydict):
	newDict = OrderedDict()
	i=0
	for item in sorted(mydict.items(), key=lambda x: x[1], reverse=True):
		newDict[item[0]] = item[1]
		i = i+1
		if (i == 10):
			break
	return newDict

def getSortedDictForKeys(keys, unsortedDict):
	tmpDict = dict()
	for key in keys:
		tmpDict[key] = unsortedDict[key]
	newDict = OrderedDict()
	for item in sorted(tmpDict.items(), key=lambda x: x[1], reverse=True):
		newDict[item[0]] = item[1]
	return newDict

BASEDIR = "/users/eprakash/projects/benchmarking/newdata/A549/models/deepseabeluga/motifs"

ig_multiref_full = getMotif2AuprcDict(BASEDIR + "/ig.txt")
ig_avg_gc_ref_full = getMotif2AuprcDict(BASEDIR + "/ig_avg_gc_ref.txt")
ig_all_zeros_ref_full = getMotif2AuprcDict(BASEDIR + "/ig_all_zeros_ref.txt")
ig_multiref = mySort(ig_multiref_full)
ig_avg_gc_ref = mySort(ig_avg_gc_ref_full)
ig_all_zeros_ref = mySort(ig_all_zeros_ref_full)

ig_multiref_keyset = set(ig_multiref.keys())
ig_avg_gc_ref_keyset = set(ig_avg_gc_ref.keys())
ig_all_zeros_ref_keyset = set(ig_all_zeros_ref.keys())


all_keys = ig_multiref_keyset.union(ig_avg_gc_ref_keyset, ig_all_zeros_ref_keyset)
all_keys_dict = getSortedDictForKeys(all_keys, ig_multiref_full)

for key in all_keys_dict.keys():
	print "" + key + " " + str(ig_multiref_full[key]) + " " + str(ig_avg_gc_ref_full[key]) + " " + str(ig_all_zeros_ref_full[key]) 
