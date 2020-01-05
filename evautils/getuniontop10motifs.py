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
rescale_conv_full = getMotif2AuprcDict(BASEDIR + "/rescale_conv.txt")
grad_times_input_full = getMotif2AuprcDict(BASEDIR + "/grad_times_input.txt")
ig_full = getMotif2AuprcDict(BASEDIR + "/ig.txt")
ism_full = getMotif2AuprcDict(BASEDIR + "/ism.txt")
rescale_all = mySort(rescale_all_full)
rescale_conv = mySort(rescale_conv_full)
grad_times_input = mySort(grad_times_input_full)
ig = mySort(ig_full)
ism  = mySort(ism_full)

rescale_all_keyset = set(rescale_all.keys())
rescale_conv_keyset = set(rescale_conv.keys())
grad_times_input_keyset = set(grad_times_input.keys())
ig_keyset = set(ig.keys())
ism_keyset = set(ism.keys())


all_keys = rescale_all_keyset.union(rescale_conv_keyset, grad_times_input_keyset, ig_keyset, ism_keyset)
all_keys_dict = getSortedDictForKeys(all_keys, rescale_all_full)

for key in all_keys_dict.keys():
	print "" + key + " " + str(rescale_conv_full[key]) + " " + str(rescale_all_full[key]) + " " + str(ig_full[key]) + " " + str(grad_times_input_full[key]) + " " + str(ism_full[key])
