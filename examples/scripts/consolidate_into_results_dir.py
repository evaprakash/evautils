#!/users/eprakash/anaconda2/bin/python

import glob
import os
import shutil
import json

RESULTS_DIR = "/users/eprakash/hyperparams_results"
TEST_DIR = "/users/eprakash/experiments/K562/GATA1"
records = {
    "dense_30" : "0LcoP",
    "dense_50" : "vAHnL",
    "dense_10" : "c8Cj2",
    "batch_norm_axis_-1" : "JMAzN",
    "batch_norm_all_activations" : "YWe2f",
    "dropout_0_2_batch_norm" : "vv9b1",
    "lr_0_0005" : "bGNjI",
    "lr_0_0001" : "EOMnp",
    "lr_0_01" : "t1jyq",
    "filter_10" : "dBFb2",
    "filter_3" : "er64g",
    "l1_l2" : "7z76M",
    "l2" : "obvUz",
    "l1" : "U6BKe",
    "l2_lambda_0_1" : "fuTnK",
    "l2_batch_norm" : "JVWPP",
    "l2_batch_norm_lambda_0_001" : "uAEGB",
    "l2_lambda_0_001" : "w6q9F",
    "add_two_conv_layers" : "fC7hO",
    "add_conv_layer" : "twk5a",
    "remove_from_end" : "hjEq8"
    }

def find_model_file_directory(model_id):
    for path, dirs, files in os.walk(TEST_DIR):
        for file in files:
            if str(model_id + "_model") in file:
                return path

def copy_model_and_weights(model_id, model_file_directory):
    previous_dir = os.getcwd()
    os.chdir(model_file_directory)
    for filename in glob.glob("*modelJson.json"):
        shutil.copy(filename, RESULTS_DIR)
        filename = filename.replace("modelJson.json", "modelWeights.h5")
        shutil.copy(filename, RESULTS_DIR)
    os.chdir(previous_dir)

def add_to_db_file(model_descriptor, model_file_directory, models_dict):
    previous_dir = os.getcwd()
    os.chdir(model_file_directory)
    os.chdir("..")
    fp = open("runs_perf-metric-auROC.db")
    data = json.load(fp)
    data = data["records"]
    models_dict["models"].update({model_descriptor : data})
    fp.close()
    os.chdir(previous_dir)

def consolidate():
    models_dict = {"models":{}}
    fp = open(RESULTS_DIR + "/model_ids.txt", 'w')
    for model_descriptor in records:
        print("On model " + model_descriptor)
        model_id = records[model_descriptor]
        fp.write(model_id + "\n")
        model_file_directory = find_model_file_directory(model_id)
        copy_model_and_weights(model_id, model_file_directory)
        add_to_db_file(model_descriptor, model_file_directory, models_dict)
    fp.close()
    fp = open(RESULTS_DIR + "/models.db", 'w')
    json.dump(models_dict, fp, indent = 4)
    fp.close()

consolidate()
