#!/users/eprakash/anaconda2/bin/python

import evautils
from evautils import sequtils
from evautils import kerasutils
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import average_precision_score
import argparse

def get_aucs(preds, true_labels):
    auroc = roc_auc_score(y_true=true_labels, y_score=preds)
    auprc = average_precision_score(y_true=true_labels, y_score=preds)
    return auroc, auprc

def get_true_labels(labels, positive_labels, negative_labels):
    true_labels=[]
    for label in labels:
        if label in positive_labels:
            true_labels.append(1)
        elif label in negative_labels:
            true_labels.append(0)
        else:
            continue
    return true_labels

def get_preds(onehot_data, keras_model):
    return keras_model.predict(onehot_data)

def get_auroc_auprc(data_filename_positive, data_filename_negative, model_file, weights_file):
    labeled_pos_sequences = sequtils.load_sequences_from_bedfile(data_filename_positive)
    labeled_neg_sequences = sequtils.load_sequences_from_bedfile(data_filename_negative)
    labeled_sequences = {}
    labeled_sequences.update(labeled_pos_sequences)
    labeled_sequences.update(labeled_neg_sequences)
    positive_labels = labeled_pos_sequences.keys()
    negative_labels = labeled_neg_sequences.keys()
    labels = labeled_sequences.keys()
    sequences = labeled_sequences.values()
    
    sequtils.removeUnsupportedChars(sequences, labels, labeled_sequences)

    onehot_data = np.array([sequtils.one_hot_encode_along_channel_axis(seq) for seq in sequences])

    keras_model=kerasutils.load_keras_model_using_json(model_file, weights_file)

    preds = get_preds(onehot_data, keras_model)

    true_labels=get_true_labels(labels, positive_labels, negative_labels)

    auroc, auprc = get_aucs(preds, true_labels)

    print("auROC: " + str(auroc))
    print("auPRC: " + str(auprc))

parser = argparse.ArgumentParser()
parser.add_argument("pos_file", type=str, help="Positive sequence gzipped bed file")
parser.add_argument("neg_file", type=str, help="Negative sequence gzipped bed file")
parser.add_argument("model_file", type=str, help="Model file")
parser.add_argument("weights_file", type=str, help="Weights file")
args = parser.parse_args()
get_auroc_auprc(args.pos_file, args.neg_file, args.model_file, args.weights_file)
