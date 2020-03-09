#!/users/eprakash/anaconda2/bin/python

import numpy as np
import re
from collections import OrderedDict

def parseMotifResults(filename):
        fp = open(filename, "r")
        motifdict = OrderedDict()
        for line in fp:
                match = re.match("(\w+):\s+\[(.+),\s+(.+),\s+(.+)\]", line)
                if match:
                        motif = match.group(1)
                        auroc = float(match.group(2))
                        auprc = float(match.group(3))
                        hits = int(float(match.group(4)))
                        motifdict[motif] = {"auroc": auroc, "auprc": auprc, "hits": hits}
        fp.close()
        return motifdict

def sortMotifDictBy(motifdict, fieldname, descending=True):
        assert(fieldname == "auroc" or fieldname == "auprc" or fieldname == "hits")
        newDict = OrderedDict()
        for item in sorted(motifdict.items(), key=lambda x: x[1][fieldname], reverse=descending):
                newDict[item[0]] = item[1]
        return newDict

def printResultsDict(resultsDict):
    for motif in resultsDict.keys():
        print(str(motif) + str(resultsDict[motif]))

def getFieldValuesForMotifs(motifdict, motiflist, fieldname):
    retval = []
    for motif in motiflist:
        val = motifdict[motif][fieldname]
        retval.append(val)
    return retval
