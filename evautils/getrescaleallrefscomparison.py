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

rescale_all_full = getMotif2AuprcDict(BASEDIR + "/rescale_all.txt")
rescale_all_avg_gc_ref_full = getMotif2AuprcDict(BASEDIR + "/rescale_all_avg_gc_ref.txt")
rescale_all_all_zeros_ref_full = getMotif2AuprcDict(BASEDIR + "/rescale_all_all_zeros_ref.txt")
rescale_all = mySort(rescale_all_full)
rescale_all_avg_gc_ref = mySort(rescale_all_avg_gc_ref_full)
rescale_all_all_zeros_ref = mySort(rescale_all_all_zeros_ref_full)

rescale_all_keyset = set(rescale_all.keys())
rescale_all_avg_gc_ref_keyset = set(rescale_all_avg_gc_ref.keys())
rescale_all_all_zeros_ref_keyset = set(rescale_all_all_zeros_ref.keys())


all_keys = rescale_all_keyset.union(rescale_all_avg_gc_ref_keyset, rescale_all_all_zeros_ref_keyset)
all_keys_dict = getSortedDictForKeys(all_keys, rescale_all_full)

for key in all_keys_dict.keys():
	print "" + key + " " + str(rescale_all_full[key]) + " " + str(rescale_all_avg_gc_ref_full[key]) + " " + str(rescale_all_all_zeros_ref_full[key]) 
