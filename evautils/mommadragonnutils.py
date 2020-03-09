#!/users/eprakash/anaconda2/bin/python

import math
import os
import evautils
from evautils import sequtils
from evautils import osutils
from collections import OrderedDict

def createTrainAndValid(posBedFile, negBedFile, posPrefix, negPrefix, posTrain, negTrain, posValid, negValid):
	osutils.runCommand('zcat ' + posBedFile + ' | head -' + str(posTrain) + ' > ' + posPrefix + '_train.bed')
	osutils.runCommand('zcat ' + negBedFile + ' | head -' + str(negTrain) + ' > ' + negPrefix + '_train.bed')
	osutils.runCommand('zcat ' + posBedFile + ' | tail -' + str(posValid) + ' > ' + posPrefix + '_valid.bed')
	osutils.runCommand('zcat ' + negBedFile + ' | tail -' + str(negValid) + ' > ' + negPrefix + '_valid.bed')
	osutils.runCommand('gzip ' + posPrefix + '_train.bed')
	osutils.runCommand('gzip ' + negPrefix + '_train.bed')
	osutils.runCommand('gzip ' + posPrefix + '_valid.bed')
	osutils.runCommand('gzip ' + negPrefix + '_valid.bed')


def splitDatasets(posBedFile, negBedFile, posPrefix, negPrefix):
	num_pos_seqs=int(osutils.runCommandCaptureOutput('zcat ' + posBedFile + ' | wc -l'))
	num_neg_seqs=int(osutils.runCommandCaptureOutput('zcat ' + posBedFile + ' | wc -l'))
	print("TOTAL POS: " + str(num_pos_seqs))
	print("TOTAL NEG: " + str(num_neg_seqs))
	num_pos_train=int(math.ceil(0.8*num_pos_seqs))
	num_pos_valid=int(num_pos_seqs-num_pos_train)
	num_neg_train=int(math.ceil(0.8*num_neg_seqs))
	num_neg_valid=int(num_neg_seqs-num_neg_train)
	print("POS TRAIN: " + str(num_pos_train))
	print("NEG TRAIN: " + str(num_neg_train))
	print("POS VALID: " + str(num_pos_valid))
	print("NEG VALID: " + str(num_neg_valid))
	createTrainAndValid(posBedFile, negBedFile, posPrefix, negPrefix, num_pos_train, num_neg_train, num_pos_valid, num_neg_valid)

def fillPlaceholders(filename, weightfile, postrain, negtrain, posvalid, negvalid, samplesPerEpoch='30', maxEpochs='300', epochsToWait='3', batchSize='50'):
	replace(filename, '__BENCHMARKING_WEIGHTFILE', weightfile)
	replace(filename, '__BENCHMARKING_POS_TRAIN', postrain)
	replace(filename, '__BENCHMARKING_NEG_TRAIN', negtrain)
	replace(filename, '__BENCHMARKING_POS_VALID', posvalid)
	replace(filename, '__BENCHMARKING_NEG_VALID', negvalid)
	replace(filename, '__BENCHMARKING_SAMPLES_PER_EPOCH', samplesPerEpoch)
	replace(filename, '__BENCHMARKING_MAX_EPOCHS', maxEpochs)
	replace(filename, '__BENCHMARKING_EPOCHS_TO_WAIT', epochsToWait)
	replace(filename, '__BENCHMARKING_BATCH_SIZE', batchSize)

def replace(filename, placeholder, value):
	tmpfilename = filename+".tmp"
        fp=open(filename)
        tmpfp=open(tmpfilename, "w+")
        for line in fp:
                line=line.replace(placeholder, value)
                tmpfp.write(line)
	os.rename(tmpfilename, filename)
        fp.close()

def runMD(md, debug=False):
	command='(cd ' + md + '; ' + md + '/run_me.sh'+')'
	osutils.runCommandRealTime(command, isShell=True, debug=debug)

#runMD('/users/eprakash/training/momma_dragonn/examples/fasta_sequential_model')
