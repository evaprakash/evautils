#!/users/eprakash/anaconda2/bin/python

import evautils
from evautils import sequtils
from evautils import kerasutils
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score
import argparse
import re

def get_aucs(preds, true_labels):
    auroc = roc_auc_score(y_true=true_labels, y_score=preds)
    auprc = average_precision_score(y_true=true_labels, y_score=preds)
    return auroc, auprc

def get_true_labels(pos_list, neg_list):
    labels = [1 for seq in pos_list] + [0 for seq in neg_list]
    return labels

def get_preds(onehot_data, keras_model):
    return keras_model.predict(onehot_data)

def get_auroc_auprc(data_filename_positive, data_filename_negative, model_file, weights_file):
    pos_sequences_dict = sequtils.load_sequences_from_bedfile(data_filename_positive)
    neg_sequences_dict = sequtils.load_sequences_from_bedfile(data_filename_negative)
    
    pos_list = list(pos_sequences_dict.values())
    neg_list = list(neg_sequences_dict.values())
    sequence_list = pos_list + neg_list

    onehot_data = np.array([sequtils.one_hot_encode_along_channel_axis(seq) for seq in sequence_list])
    keras_model = kerasutils.load_keras_model_using_json(model_file, weights_file)
    preds = get_preds(onehot_data, keras_model)

    labels = get_true_labels(sequence_list, pos_list, neg_list)
    auroc, auprc = get_aucs(preds, labels)

    print("auROC: " + str(auroc))
    print("auPRC: " + str(auprc))

parser = argparse.ArgumentParser()
parser.add_argument("pos_file", type=str, help="Positive sequence gzipped bed file")
parser.add_argument("neg_file", type=str, help="Negative sequence gzipped bed file")
parser.add_argument("model_file", type=str, help="Model file")
parser.add_argument("weights_file", type=str, help="Weights file")
args = parser.parse_args()
get_auroc_auprc(args.pos_file, args.neg_file, args.model_file, args.weights_file)
