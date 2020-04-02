#!/users/eprakash/anaconda2/bin/python
import keras
import argparse
import evautils
from evautils import sequtils
from evautils import kerasutils
from collections import OrderedDict
import numpy as np
import h5py

def get_perturbed_seqs(scores, original_encoded_seqs):
    sorted_score_indices = np.argsort(scores, axis=1)
    num_seqs = scores.shape[0]
    total_pos = scores.shape[1]
    twenty_percent_pos = total_pos/5
    displacements = np.random.randint(1, high=4, size=(num_seqs, twenty_percent_pos))
    perturbed_seqs = []
    for seq in range(0, num_seqs):
        perturbed = [(original_encoded_seqs[seq][sorted_score_indices[seq][pos]] + displacements[seq][pos]) % 4 for pos in range (0, twenty_percent_pos)]
        remaining = [original_encoded_seqs[seq][pos] for pos in range (twenty_percent_pos, total_pos)]
        perturbed.extend(remaining)
        perturbed_seqs.append(perturbed)
    return np.array(perturbed_seqs)
    
def get_imp_score_info_and_seq_ids(imp_score_file):
    method_to_scores = OrderedDict()
    f = h5py.File(imp_score_file, 'r')
    methods = list(f.keys())[:-1]
    for method in methods:
        method_to_scores.update({method : np.array(f.get(method))})
    seq_ids = list(f.get(f.keys()[-1]))
    print(type(seq_ids))
    f.close()
    return method_to_scores, seq_ids

def decode_seq(seq):
    decoded_seq = ""
    for index in range(0, len(seq)):
        base = seq[index]
        if base == 1:
            decoded_seq += 'G'
        elif base == 2:
            decoded_seq += 'C'
        elif base == 3:
            decoded_seq += 'T'
        elif base == 0:
            decoded_seq += 'A'
        else:
            decoded_seq += 'N'
    return decoded_seq


def encode_seq(seq):
    encoded_seq = np.zeros(len(seq))
    for index in range(0, len(seq)):
        base = seq[index]
        if base == 'G':
            encoded_seq[index] = 1
        elif base == 'C':
            encoded_seq[index] = 2
        elif base == 'T':
            encoded_seq[index] = 3
        elif base != 'A':
            encoded_seq[index] = 4
    return encoded_seq

def get_preds(onehot_data, keras_model):
    return keras_model.predict(onehot_data)

def perturbation_evaluation(model_file, weights_file, seq_file, imp_score_file, output_file):
    method_to_scores, seq_ids = get_imp_score_info_and_seq_ids(imp_score_file)
    sequence_dict = sequtils.load_sequences_from_bedfile(seq_file)
    sequence_list = [sequence_dict[seq] for seq in seq_ids]
    original_onehot_data = np.array([sequtils.one_hot_encode_along_channel_axis(seq) for seq in sequence_list])
    original_model = kerasutils.load_keras_model_using_json(model_file, weights_file)
    logit_model = keras.models.Model(input=original_model.input, output=original_model.layers[-2].output)
    original_preds = get_preds(original_onehot_data, logit_model)
    original_encoded_seqs = np.array([encode_seq(seq) for seq in sequence_list])
    f = h5py.File(output_file, 'w')
    for method in method_to_scores:
        perturbed_seqs = get_perturbed_seqs(method_to_scores[method], original_encoded_seqs)
        perturbed_decoded_seqs = np.array([decode_seq(seq) for seq in perturbed_seqs])
        perturbed_onehot_data = np.array([sequtils.one_hot_encode_along_channel_axis(seq) for seq in perturbed_decoded_seqs])
        perturbed_preds = get_preds(perturbed_onehot_data, logit_model)
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
    args = parser.parse_args()
    perturbation_evaluation(args.model_file, args.weights_file, args.seq_file, args.imp_score_file, args.output_h5_file)
