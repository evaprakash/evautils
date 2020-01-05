#!/users/eprakash/anaconda2/bin/python

import numpy as np
import keras
import deeplift
import tensorflow as tf
from keras.models import model_from_json
from keras.models import load_model
from deeplift.util import compile_func
from keras.models import model_from_json
from deeplift.layers import NonlinearMxtsMode
import deeplift.conversion.kerasapi_conversion as kc
reload(deeplift.layers)
reload(deeplift.conversion.kerasapi_conversion)
from collections import OrderedDict

def load_keras_model_using_json(json_file_name, h5_weights_file):
    json_file = open(json_file_name, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    print("Loading Keras JSON model from file " + json_file_name)
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    print("Loading Keras model weights from file " + h5_weights_file)
    loaded_model.load_weights(h5_weights_file)
    print("Successfully loaded")
    return loaded_model

def createTrueLabels(labels, positive_labels, negative_labels):
	true_labels=[]
	for label in labels:
	    if label in positive_labels:
	        true_labels.append(1)
	    elif label in negative_labels:
	        true_labels.append(0)
	    else:
	        continue
	print(len(true_labels))
	return true_labels

def seqsToPreds(labels, positive_labels, preds):
	seq_id_to_pred={}
	for index in range(0,len(labels)):
	    label=labels[index]
	    if label in positive_labels:
	        seq_id_to_pred.update({label:preds[index][0]})
	print(len(seq_id_to_pred))
	print(len(positive_labels))
	return seq_id_to_pred

def getTopNumPos(labels, labeled_sequences, preds, num):
	seq_id_to_pred=seqsToPreds(labels, labels, preds)
	top_num_pos_labels=sorted(seq_id_to_pred, key=lambda x: seq_id_to_pred[x])[-num:]
	top_num_pos=[]
	for label in top_num_pos_labels:
	    top_num_pos.append(labeled_sequences[label])
	return top_num_pos_labels, top_num_pos

def prepareDLModel(weights, model):
	method_to_model = OrderedDict()
	for method_name, nonlinear_mxts_mode in [
	    #The genomics default = rescale on conv layers, revealcance on fully-connected
	    ('rescale_conv_revealcancel_fc', NonlinearMxtsMode.DeepLIFT_GenomicsDefault),
	    ('rescale_all_layers', NonlinearMxtsMode.Rescale),
	    ('revealcancel_all_layers', NonlinearMxtsMode.RevealCancel),
	    ('grad_times_inp', NonlinearMxtsMode.Gradient),
	    ('guided_backprop', NonlinearMxtsMode.GuidedBackprop)]:
	    method_to_model[method_name] = kc.convert_model_from_saved_files(
	        h5_file=weights,
	        json_file=model,
	        nonlinear_mxts_mode=nonlinear_mxts_mode)
	return method_to_model

def sanityCheck(model_to_test, onehot_data, keras_model):
	deeplift_prediction_func = compile_func([model_to_test.get_layers()[0].get_activation_vars()],
                                         model_to_test.get_layers()[-1].get_activation_vars())
	original_model_predictions = keras_model.predict(onehot_data, batch_size=200)
	converted_model_predictions = deeplift.util.run_function_in_batches(
                                input_data_list=[onehot_data],
                                func=deeplift_prediction_func,
                                batch_size=200,
                                progress_update=None)
	print("maximum difference in predictions:",np.max(np.array(converted_model_predictions)-np.array(original_model_predictions)))
	assert np.max(np.array(converted_model_predictions)-np.array(original_model_predictions)) < 10**-5
	predictions = converted_model_predictions
