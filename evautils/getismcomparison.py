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

ism_full = getMotif2AuprcDict(BASEDIR + "/ism.txt")
ism_abs_full = getMotif2AuprcDict(BASEDIR + "/ism_abs.txt")
ism = mySort(ism_full)
ism_abs = mySort(ism_abs_full)

ism_keyset = set(ism.keys())
ism_abs_keyset = set(ism_abs.keys())


all_keys = ism_keyset.union(ism_abs_keyset)
all_keys_dict = getSortedDictForKeys(all_keys, ism_full)

for key in all_keys_dict.keys():
	print "" + key + " " + str(ism_full[key]) + " " + str(ism_abs_full[key]) 
