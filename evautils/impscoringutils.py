#!/users/eprakash/anaconda2/bin/python

import numpy as np
import evautils
from evautils import sequtils
import deeplift
from collections import OrderedDict
reload(deeplift.util)
from deeplift.util import get_shuffle_seq_ref_function
from deeplift.dinuc_shuffle import dinuc_shuffle

def compileScoringFunctions(method_to_model):
	print("Compiling scoring functions")
	method_to_scoring_func = OrderedDict()
	for method, model in method_to_model.items():
	    print("Compiling scoring function for: "+method)
	    method_to_scoring_func[method] = model.get_target_contribs_func(find_scores_layer_idx=0,
                                                                    target_layer_idx=-2)
    
	#To get a function that just gives the gradients, we use the multipliers of the Gradient model
	gradient_func = method_to_model['grad_times_inp'].get_target_multipliers_func(find_scores_layer_idx=0,
                                                                              target_layer_idx=-2)
	print("Compiling integrated gradients scoring functions")
	integrated_gradients10_func = deeplift.util.get_integrated_gradients_function(
	    gradient_computation_function = gradient_func,
	    num_intervals=10)
	method_to_scoring_func['integrated_gradients10'] = integrated_gradients10_func
	return method_to_scoring_func

def multirefScore(method_to_task_to_scores, method_to_scoring_func, methods_list, sequences):
	for method in methods_list:
		print("On method " + method)
		many_refs_func = get_shuffle_seq_ref_function(
	    	score_computation_function=method_to_scoring_func[method],
	    	shuffle_func=dinuc_shuffle,
    		one_hot_func=lambda x: np.array([sequtils.one_hot_encode_along_channel_axis(seq) for seq in x]))

		num_refs_per_seq=10
		method_to_task_to_scores[method+'_multiref_'+str(num_refs_per_seq)] = OrderedDict()
		for task_idx in [0]:
  	 		 method_to_task_to_scores[method+'_multiref_'+str(num_refs_per_seq)][task_idx] =\
        		 np.sum(many_refs_func(
		            task_idx=task_idx,
            		    input_data_sequences=sequences,
		            num_refs_per_seq=num_refs_per_seq,
		            batch_size=200,
		            progress_update=1000,
		            ),axis=2)


def flatRefScore(method_to_task_to_scores, method_to_scoring_func, methods_list, onehot_data, refOption):
	if (refOption == 0):
		background = OrderedDict([('A', 0.0), ('C', 0.0), ('G', 0.0), ('T', 0.0)])
	else:
		avg_gc_content = np.mean(onehot_data, axis=(0,1))
		print(avg_gc_content)
		background = OrderedDict([('A', avg_gc_content[0]), ('C', avg_gc_content[1]), ('G', avg_gc_content[2]), ('T', avg_gc_content[3])])
		print(background)
	print (method_to_scoring_func.keys())
	for method_name, score_func in method_to_scoring_func.items():
	    print("on method",method_name)
	    print("scorefunc ", score_func)
	    if (method_name not in methods_list):
	        continue
	    if (refOption == 0):
		method_variation=method_name + "_all_zeros_ref"
	    else:
		method_variation=method_name + "_avg_gc_ref"
	    method_to_task_to_scores[method_variation] = OrderedDict()
	    for task_idx in [0]:
	        print("On method variation: " + method_variation)
		scores = np.array(score_func(
				   	task_idx=task_idx,
				        input_data_list=[onehot_data],
				        input_references_list=[
						        np.array([background['A'],
					                background['C'],
					                background['G'],
					                background['T']])[None,None,:]],
					batch_size=200,
					progress_update=None))
        	assert scores.shape[2]==4
	        scores = np.sum(scores, axis=2)
		method_to_task_to_scores[method_variation][task_idx] = scores
