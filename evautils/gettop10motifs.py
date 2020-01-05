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

BASEDIR = "/users/eprakash/projects/benchmarking/newdata/GM12878/models/deepseabeluga/motifs"

rescale_all = mySort(getMotif2AuprcDict(BASEDIR + "/rescale_all.txt"))
rescale_conv = mySort(getMotif2AuprcDict(BASEDIR + "/rescale_conv.txt"))
grad_times_input = mySort(getMotif2AuprcDict(BASEDIR + "/grad_times_input.txt"))
ig = mySort(getMotif2AuprcDict(BASEDIR + "/ig.txt"))
ism  = mySort(getMotif2AuprcDict(BASEDIR + "/ism.txt"))

rescale_all_keyset = set(rescale_all.keys())
rescale_conv_keyset = set(rescale_conv.keys())
grad_times_input_keyset = set(grad_times_input.keys())
ig_keyset = set(ig.keys())
ism_keyset = set(ism.keys())

common_keys = rescale_all_keyset.intersection(rescale_conv_keyset, grad_times_input_keyset, ig_keyset, ism_keyset)

for key in rescale_all.keys():
	if key in common_keys:
		print "" + key + " " + str(rescale_conv[key]) + " " + str(rescale_all[key]) + " " + str(ig[key]) + " " + str(grad_times_input[key]) + " " + str(ism[key])
