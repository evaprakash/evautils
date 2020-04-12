#!/usr/bin/env python
import keras
import argparse
import evautils
from evautils import sequtils
from evautils import kerasutils
from collections import OrderedDict
import numpy as np
import h5py
import deeplift
from deeplift import dinuc_shuffle
import tensorflow as tf

def get_shuffled_seqs(onehot_seqs):
    #pregenerate the shuffling
    max_num_shuffref = 10
    shuffled_seqs = []
    for i in range(len(onehot_seqs)):
        rng = np.random.RandomState(1234)
        if (i%100==0):
            print("Generating shuffled seqs for seq "+str(i))
        shuffled_seqs.append([
            dinuc_shuffle.dinuc_shuffle(s=onehot_seqs[i], rng=rng) for x in range(max_num_shuffref)])
    shuffled_seqs = np.array(shuffled_seqs)
    return shuffled_seqs, max_num_shuffref

def get_perturbed_seqs(scores, original_onehot_data, is_lowest):
    sorted_score_indices = np.argsort(scores, axis=1)
    num_seqs = int(scores.shape[0])
    total_pos = int(scores.shape[1])
    if (is_lowest):
        modifiable = list(range(int(total_pos/5)))
    else:
        modifiable = list(range(int(4*total_pos/5), total_pos))
    shuffled_seqs, max_num_shuffref = get_shuffled_seqs(original_onehot_data)
    perturbed_seqs = np.zeros((num_seqs, max_num_shuffref, total_pos, 4), dtype=int)
    for seq in range(num_seqs):
        perturbed_seqs[seq][:] = original_onehot_data[seq]
    for seq in range(num_seqs):
        replacement_pos = sorted_score_indices[seq][modifiable]
        for shuff_num in range(max_num_shuffref):
            perturbed_seqs[seq][shuff_num][replacement_pos] = shuffled_seqs[seq][shuff_num][replacement_pos]
    return perturbed_seqs, max_num_shuffref

def get_imp_score_info_and_seq_ids(imp_score_file, is_lowest):
    method_to_scores = OrderedDict()
    f = h5py.File(imp_score_file, 'r')
    methods = list(f.keys())[:-1]
    for method in methods:
        if (is_lowest):
            method_to_scores.update({method : np.absolute(np.array(f.get(method)))})
        else:
            method_to_scores.update({method : np.array(f.get(method))})
    seq_ids = list(f.get(list(f.keys())[-1]))
    print(type(seq_ids))
    f.close()
    return method_to_scores, seq_ids

def get_preds(onehot_data, keras_model):
    return keras_model.predict(onehot_data)

def perturbation_evaluation(model_file, weights_file, seq_file, imp_score_file, output_file, is_lowest):
    #Added following statement to limit number of cores used
    #tf.config.threading.set_intra_op_parallelism_threads(1)
    #tf.config.threading.set_inter_op_parallelism_threads(1)
    print (is_lowest)
    method_to_scores, seq_ids = get_imp_score_info_and_seq_ids(imp_score_file, is_lowest)
    sequence_dict = sequtils.load_sequences_from_bedfile(seq_file)
    sequence_list = [sequence_dict[seq.decode()] for seq in seq_ids]
    original_onehot_data = np.array([sequtils.one_hot_encode_along_channel_axis(seq) for seq in sequence_list])
    original_model = kerasutils.load_keras_model_using_json(model_file, weights_file)
    logit_model = keras.models.Model(input=original_model.input, output=original_model.layers[-2].output)
    original_preds = get_preds(original_onehot_data, logit_model)
    f = h5py.File(output_file, 'w')
    for method in method_to_scores:
        perturbed_onehot_data, max_num_shuffref = get_perturbed_seqs(method_to_scores[method], original_onehot_data, is_lowest)
        perturbed_preds = np.zeros(original_preds.shape)
        for seq in range(len(sequence_list)):
            shuffref_preds = get_preds(perturbed_onehot_data[seq], logit_model)
            perturbed_preds[seq] = (np.sum(shuffref_preds))/max_num_shuffref
        if (is_lowest):
            differences = np.absolute(original_preds - perturbed_preds)
        else:
            differences = original_preds - perturbed_preds
        f.create_dataset(method, data=differences)
    f.close()

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_file", required=True)
    parser.add_argument("--weights_file", required=True)
    parser.add_argument("--seq_file", required=True)
    parser.add_argument("--imp_score_file", required=True)
    parser.add_argument("--output_h5_file", required=True)
    parser.add_argument("--is_lowest", required=True)
    args = parser.parse_args()
    perturbation_evaluation(args.model_file, args.weights_file, args.seq_file, args.imp_score_file, args.output_h5_file, args.is_lowest)
