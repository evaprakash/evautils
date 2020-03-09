#!/users/eprakash/anaconda2/bin/python

import numpy as np
import re
from collections import OrderedDict
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    roc_curve, precision_recall_curve)

def displayResults(directory, method_list, top_motif_ids, methods_to_plot_list, motif_id_to_motif_length, motif_id_to_hit_locations, motif_len_to_negatives, method_to_seq_id_to_scores, motif_id_to_pos_locs, appendToFileName=""):
	motif_info={}
	for method_name in method_list:
		motif_info.update({method_name:{}})
	print("Number of motifs is " + str(len(motif_id_to_motif_length.keys())))
	for motif_id in sorted(top_motif_ids):
	    for methods_to_plot in methods_to_plot_list:
	        motif_len = motif_id_to_motif_length[motif_id]
	        pos_locs = motif_id_to_hit_locations[motif_id]
	        neg_locs = motif_len_to_negatives[motif_len]
	        all_locs = list(pos_locs)+list(neg_locs)
	        loc_labels = [1 for x in pos_locs]+[0 for x in neg_locs]

	        pos_frac = float(len(pos_locs))/(len(pos_locs)+len(neg_locs))
	        for method_name in methods_to_plot:
	            seq_id_to_windowsums = {}
	            seq_id_to_scores=method_to_seq_id_to_scores[method_name]
	            for seq_id,scores in seq_id_to_scores.items():
	                cumsum = np.array([0]+list(np.cumsum(scores)))
	                windowsums = cumsum[motif_len:]-cumsum[:-motif_len]
	                seq_id_to_windowsums[seq_id] = windowsums
	            loc_scores = [seq_id_to_windowsums[seq_id][pos]
  	                        for (seq_id, pos) in all_locs]
	            auroc = roc_auc_score(y_true=loc_labels,
	                                  y_score=loc_scores)
	            auprc = average_precision_score(y_true=loc_labels,
	                                            y_score=loc_scores)
	            motif_info[method_name].update({motif_id:[auroc,auprc,motif_id_to_pos_locs[motif_id]]})

	for method_name in method_list:
		fp=open(directory+'/'+method_name+appendToFileName+'.txt', 'w+')
		print("\n")
		print(method_name+"\n")
		#fp.write(method_name+"\n")
		sorted_keys=(sorted(motif_info[method_name], key=lambda x: motif_info[method_name][x][1]))
		for key in sorted_keys[::-1]:
    			print(key+": "+str(motif_info[method_name][key]))
			fp.write(key+": "+str(motif_info[method_name][key])+"\n")
		fp.close()
	print("\n")

def motifToPosLocs(motif_id_to_pos_locs, motif_id_to_hit_locations, motif_id_to_motif_length):
	for motif_id in motif_id_to_hit_locations:
    		motif_len = motif_id_to_motif_length[motif_id]
  		num_pos_locs = len(motif_id_to_hit_locations[motif_id])
  		motif_id_to_pos_locs.update({motif_id:float(num_pos_locs)})
	print(len(motif_id_to_pos_locs))

def topEnrichedMotifs(motif_id_to_pos_locs):
	 return sorted(motif_id_to_pos_locs, key=lambda x: motif_id_to_pos_locs[x])

def collectSeqIdToScoresForAllMethods(method_to_saved_scores, seq_ids_of_interest, relevant_labels_list, ig_seq_ids_of_interest, method_to_seq_id_to_scores, ism_labels):
     for method_name in method_to_saved_scores:
            scores = method_to_saved_scores[method_name]
            if (method_name=='integrated_gradients_multiref'):
                assert(len(ig_seq_ids_of_interest)==len(scores))
                seq_id_to_scores = dict(zip(ig_seq_ids_of_interest,scores))
            elif (method_name=='ism'):
                assert(len(ism_labels)==len(scores))
                seq_id_to_scores = dict(zip(ism_labels,scores))
            else:
                print("len(seq_ids_of_interest): " + str(len(seq_ids_of_interest)))
                print("len(scores): " + str(len(scores)))
                assert(len(seq_ids_of_interest)==len(scores))
                seq_id_to_scores = dict(zip(relevant_labels_list,scores))
            method_to_seq_id_to_scores[method_name] = seq_id_to_scores

def computeAndAccumulateEmbeddings(seq_len, seq_ids_of_interest, motif_matches, seq_id_to_covered_positions, motif_id_to_hit_locations, motif_id_to_motif_length):
    new_sequences_seen = 0
    for seq_id in motif_matches:
        if (seq_id in seq_ids_of_interest):
            if (seq_id not in seq_id_to_covered_positions.keys()):
                new_sequences_seen = new_sequences_seen+1
                embedded_positions = np.zeros(seq_len)
                for embedding in motif_matches[seq_id]:
                     the_seq=embedding['sequence']
                     motif_start_loc = embedding['begin']
                     motif_end_loc = embedding['end']
                     motif_len = motif_end_loc-motif_start_loc
                     embedded_positions[motif_start_loc:motif_end_loc] = 1.0
                     motif_name = re.match('(\d+)-(\w+)-(\d+)',embedding['motif']).group(2)
                     if (motif_name in motif_id_to_motif_length):
                         assert (motif_id_to_motif_length[motif_name]==motif_len)
                     else:
                         motif_id_to_motif_length[motif_name] = motif_len
                     motif_id_to_hit_locations[motif_name].append((seq_id,motif_start_loc))
                seq_id_to_covered_positions[seq_id] = embedded_positions
    print("Saw " + str(new_sequences_seen) + " new sequences")

    total_motif_bases = 0
    total_bases = 0
    for (seqname, arr) in seq_id_to_covered_positions.items():
        total_motif_bases = total_motif_bases + np.sum(arr)
        total_bases = total_bases +  len(arr)
    print("Motif positions: " + str(total_motif_bases) + ", total positions: " + str(total_bases))

def computeMotifLenToNegatives(seq_id_to_covered_positions, motif_id_to_motif_length, motif_len_to_negatives):
    for motif_len in set(motif_id_to_motif_length.values()):
        for seq_id,covered_positions in seq_id_to_covered_positions.items():
            cumsum = np.array([0]+list(np.cumsum(covered_positions)))
            window_sums = cumsum[motif_len:]-cumsum[0:-motif_len]
            null_windows = [(seq_id,x) for x in
                            np.nonzero(window_sums==0)[0]]
            motif_len_to_negatives[motif_len].extend(null_windows)


