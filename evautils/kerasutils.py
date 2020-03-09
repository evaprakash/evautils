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

def createDLModel(weights, model, nlmxtsmode):
    return kc.convert_model_from_saved_files(
                h5_file=weights,
                json_file=model,
                nonlinear_mxts_mode=nlmxtsmode)

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

def sanityCheckGivenPredFunc(deeplift_prediction_func, onehot_data, keras_model):
        original_model_predictions = keras_model.predict(onehot_data, batch_size=200)
        converted_model_predictions = deeplift.util.run_function_in_batches(
                                input_data_list=[onehot_data],
                                func=deeplift_prediction_func,
                                batch_size=200,
                                progress_update=None)
        print("maximum difference in predictions:",np.max(np.array(converted_model_predictions)-np.array(original_model_predictions)))
        assert np.max(np.array(converted_model_predictions)-np.array(original_model_predictions)) < 10**-5
        predictions = converted_model_predictions


def list_wrapper(func):
    def wrapped_func(input_data_list, **kwargs):
        if (isinstance(input_data_list, list)):
            remove_list_on_return=False
        else:
            remove_list_on_return=True
            input_data_list = [input_data_list]
        to_return = func(input_data_list=input_data_list,
                         **kwargs)
        return to_return
    return wrapped_func

def empty_ism_buffer(results_arr,
                     input_data_onehot,
                     perturbed_inputs_preds,
                     perturbed_inputs_info):
    for perturbed_input_pred,perturbed_input_info\
        in zip(perturbed_inputs_preds, perturbed_inputs_info):
        example_idx = perturbed_input_info[0]
        if (perturbed_input_info[1]=="original"):
            results_arr[example_idx] +=\
                (perturbed_input_pred*input_data_onehot[example_idx])
        else:
            pos_idx,base_idx = perturbed_input_info[1]
            results_arr[example_idx,pos_idx,base_idx] = perturbed_input_pred

def make_ism_func(prediction_func,
                  flank_around_middle_to_perturb,
                  batch_size=200):
    @list_wrapper
    def ism_func(input_data_list, progress_update=10000, **kwargs):
        assert len(input_data_list)==1
        input_data_onehot=input_data_list[0]

        results_arr = np.zeros_like(input_data_onehot).astype("float64")

        perturbed_inputs_info = []
        perturbed_onehot_seqs = []
        perturbed_inputs_preds = []
        num_done = 0
        for i,onehot_seq in enumerate(input_data_onehot):
            perturbed_onehot_seqs.append(onehot_seq)
            perturbed_inputs_info.append((i,"original"))
            for pos in range(int(len(onehot_seq)/2)-flank_around_middle_to_perturb,
                             int(len(onehot_seq)/2)+flank_around_middle_to_perturb):
                for base_idx in range(4):
                    if onehot_seq[pos,base_idx]==0:
                        assert len(onehot_seq.shape)==2
                        new_onehot = np.zeros_like(onehot_seq) + onehot_seq
                        new_onehot[pos,:] = 0
                        new_onehot[pos,base_idx] = 1
                        perturbed_onehot_seqs.append(new_onehot)
                        perturbed_inputs_info.append((i,(pos,base_idx)))
                        num_done += 1
                        if ((progress_update is not None)
                            and num_done%progress_update==0):
                            print("Done",num_done)
                        if (len(perturbed_inputs_info)>=batch_size):
                            empty_ism_buffer(
                                 results_arr=results_arr,
                                 input_data_onehot=input_data_onehot,
                                 perturbed_inputs_preds=
                                  prediction_func([perturbed_onehot_seqs]),
                                 perturbed_inputs_info=perturbed_inputs_info)
                            perturbed_inputs_info = []
                            perturbed_onehot_seqs = []
        if (len(perturbed_inputs_info)>0):
            empty_ism_buffer(
                 results_arr=results_arr,
                 input_data_onehot=input_data_onehot,
                 perturbed_inputs_preds=
                  prediction_func([perturbed_onehot_seqs]),
                 perturbed_inputs_info=perturbed_inputs_info)
        perturbed_inputs_info = []
        perturbed_onehot_seqs = []
        results_arr = results_arr - np.mean(results_arr,axis=-1)[:,:,None]
        return input_data_onehot*results_arr
    return ism_func
