#!/users/eprakash/anaconda2/bin/python

import fnmatch
import os

BASE_DIR='/users/eprakash/experiments/K562/GATA1'
matches = []
for root, dirnames, filenames in os.walk(BASE_DIR):
    for filename in fnmatch.filter(filenames, '*auroc_auprc.txt'):
        matches.append(os.path.join(root, filename))

print 'auroc\tauprc\tfilename'
for match in matches:
    f = open(match, "r")
    (auroc_str, auroc) = (f.readline()).split()
    (auprc_str, auprc) = (f.readline()).split()
    auroc = float(auroc)
    auprc = float(auprc)
    print '{0:5.3f}\t{1:5.3f}\t{2}'.format(auroc, auprc, match)
