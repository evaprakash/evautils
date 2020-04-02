#!/users/eprakash/anaconda2/bin/python

import glob
import evautils
from evautils import osutils
import os

BASE="/users/eprakash/experiments/K562/GATA1"
FOLDERS=[
        "batch_norm/batch_norm_all_activations",
        "batch_norm/batch_norm_axis_-1",
        "conv_layers/add_conv_layer",
        "conv_layers/add_two_conv_layers",
        "conv_layers/remove_from_end",
        "dropout/dropout_0_2_batch_norm",
        "filter/filter_10",
        "filter/filter_3",
        "learning_rate/lr_0_0001",
        "learning_rate/lr_0_0005",
        "learning_rate/lr_0_01",
        "regularization/l1",
        "regularization/l1_l2",
        "regularization/l2",
        "regularization/l2_batch_norm",
        "regularization/l2_batch_norm_lambda_0_001",
        "regularization/l2_lambda_0_001",
        "regularization/l2_lambda_0_1",
        "dense/dense_10",
        "dense/dense_30",
        "dense/dense_50"
        ]
#POSITIVE_SEQS_FILE="/users/eprakash/experiments/K562/GATA1/data/train_sim_positives.txt.gz"
#NEGATIVE_SEQS_FILE="/users/eprakash/experiments/K562/GATA1/data/train_sim_negatives.txt.gz"
POSITIVE_SEQS_FILE="/users/eprakash/experiments/K562/GATA1/data/test_sim_positives.txt.gz"
NEGATIVE_SEQS_FILE="/users/eprakash/experiments/K562/GATA1/data/test_sim_negatives.txt.gz"
AUROC_PRC_CMD="/users/eprakash/evautils/examples/scripts/get_auroc_auprc.py"


for folder in FOLDERS:
    topfolder = BASE + "/" + folder;
    modelsfolder = topfolder + "/momma_dragonn/examples/fasta_sequential_model/model_files"
    os.chdir(modelsfolder)
    for filename in glob.glob("*modelJson.json"):
        modelid = filename.replace("modelJson.json", "")
        modelJson = modelsfolder + "/" + modelid + "modelJson.json"
        modelWeights = modelsfolder + "/" + modelid + "modelWeights.h5"
        outputfile = topfolder + "/" + modelid + "test_auroc_auprc.txt"
        cmd = "python " + AUROC_PRC_CMD + " " + POSITIVE_SEQS_FILE + " " + NEGATIVE_SEQS_FILE + " " + modelJson + " " + modelWeights + " " + outputfile 
        osutils.runCommandRealTime(cmd)
