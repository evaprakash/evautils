#!/usr/bin/python

import evautils
from evautils import sequtils
import re
import gzip
import os
from collections import OrderedDict
import random
import matplotlib.pyplot as plt
import numpy as np

def gc_content(seq):
    g_count=seq.lower().count('g')
    c_count=seq.lower().count('c')
    return float(g_count+c_count)/float(len(seq))

def sample_matched_bqtls(bqtls_to_match, bqtls_to_sample, attrfunc, display):
    #sort bqtls_to_sample by the attribute
    sorted_bqtls_to_sample = sorted([x for x in bqtls_to_sample
                                     if np.isnan(attrfunc(x))==False],
                                    key=lambda x: attrfunc(x))
    #create a list of just the attribute values from the sorted items
    sorted_bqtls_to_sample_vals = [attrfunc(x) for x in sorted_bqtls_to_sample]
    
    bqtls_to_match_vals = [attrfunc(x) for x in bqtls_to_match]

    #for each value in the set to match, find the index in sorted_bqtls_to_sample_vals that matches it best
    searchsorted_indices = np.searchsorted(a=sorted_bqtls_to_sample_vals, v=bqtls_to_match_vals)
    
    matched_sampled_bqtls_indices = set()
    
    for idx in searchsorted_indices:
        #if the index you are considering sampling has already been sampled in a previous step, shift the index around until you find an index that isn't taken
        shift = 1
        while (idx in matched_sampled_bqtls_indices or idx==len(sorted_bqtls_to_sample)):
            #if you are about to go over the end of the list in your search for an index that is not taken, start searching in the other direction
            if idx == len(sorted_bqtls_to_sample):
                shift = -1
            idx += shift
        if (idx < 0 or idx > len(sorted_bqtls_to_sample)):
            print(idx) #this print statement shouldn't be triggered unless the set you are trying to match is bigger than the set you are subsampling from
        matched_sampled_bqtls_indices.add(idx)
    
    matched_sampled_bqtls = [sorted_bqtls_to_sample[idx] for idx in sorted(matched_sampled_bqtls_indices)]
    
    #compare the two distributions to see if they match well
    if (display):
        import seaborn as sns
        sns.distplot([attrfunc(x) for x in bqtls_to_match], color='blue')
        sns.distplot([attrfunc(x) for x in matched_sampled_bqtls], color='red')
        plt.show()

    return matched_sampled_bqtls

def match_gc_content(posFastaFile, negFastaFile, matchedNegFastaFile, display=True):
	pos_seqs_dict= sequtils.load_sequences(posFastaFile)
	neg_seqs_dict= sequtils.load_sequences(negFastaFile)
	pos_labels=pos_seqs_dict.keys()
	random.shuffle(pos_labels)
	neg_labels=neg_seqs_dict.keys()
	random.shuffle(neg_labels)
	pos_seqs=[]
	for label in pos_labels:
		pos_seqs.append(pos_seqs_dict[label])
	neg_seqs=[]
	for label in neg_labels:
		neg_seqs.append(neg_seqs_dict[label])
	
	matched_sampled_negatives=sample_matched_bqtls(bqtls_to_match=pos_seqs, bqtls_to_sample=neg_seqs, attrfunc=gc_content, display=display)
	
	random.shuffle(matched_sampled_negatives)
	
	matched_neg_seqs=OrderedDict()
	for matched_seq in matched_sampled_negatives:
		idx=neg_seqs.index(matched_seq)
		matched_neg_seqs.update({neg_labels[idx]:neg_seqs[idx]})

	fp = open(matchedNegFastaFile, "w")
	idx=0
	for matched_seq_key in matched_neg_seqs.keys():
		fp.write('>'+matched_seq_key+'\n')
		if idx==len(matched_neg_seqs)-1:
        		fp.write(matched_neg_seqs[matched_seq_key])
		else:
        		fp.write(matched_neg_seqs[matched_seq_key]+'\n')
	fp.close()

def gc_sanity_check(posBedFile, negBedFile, display=True):
	pos_seqs_dict= sequtils.load_sequences_from_bedfile(posBedFile)
        neg_seqs_dict= sequtils.load_sequences_from_bedfile(negBedFile)
        pos_labels=pos_seqs_dict.keys()
        random.shuffle(pos_labels)
        neg_labels=neg_seqs_dict.keys()
        random.shuffle(neg_labels)
        pos_seqs=[]
        for label in pos_labels:
                pos_seqs.append(pos_seqs_dict[label])
        neg_seqs=[]
        for label in neg_labels:
                neg_seqs.append(neg_seqs_dict[label])
        matched_sampled_negatives=sample_matched_bqtls(bqtls_to_match=pos_seqs, bqtls_to_sample=neg_seqs, attrfunc=gc_content, display=display)
	os.system('gzip ' + posBedFile)
	os.system('gzip ' + negBedFile)
