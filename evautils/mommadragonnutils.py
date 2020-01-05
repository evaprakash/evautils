#!/users/eprakash/anaconda2/bin/python

import math
import os
import evautils
from evautils import sequtils
from evautils import osutils
from collections import OrderedDict

def createTrainAndValid(posBedFile, negBedFile, posPrefix, negPrefix, posTrain, negTrain, posValid, negValid):
	os.system('zcat ' + posBedFile + ' | head -' + str(int(posTrain)) + ' > ' + posPrefix + '_train.bed')
	os.system('zcat ' + negBedFile + ' | head -' + str(int(negTrain)) + ' > ' + negPrefix + '_train.bed')
	os.system('zcat ' + posBedFile + ' | tail -' + str(int(posValid)) + ' > ' + posPrefix + '_valid.bed')
	os.system('zcat ' + negBedFile + ' | tail -' + str(int(negValid)) + ' > ' + negPrefix + '_valid.bed')
	os.system('gzip ' + posPrefix + '_train.bed')
	os.system('gzip ' + negPrefix + '_train.bed')
	os.system('gzip ' + posPrefix + '_valid.bed')
	os.system('gzip ' + negPrefix + '_valid.bed')


def splitDatasets(posBedFile, negBedFile, posPrefix, negPrefix):
	num_pos_seqs=sequtils.count_seqs(posBedFile)
	num_neg_seqs=sequtils.count_seqs(negBedFile)
	print("TOTAL POS: " + str(num_pos_seqs))
	print("TOTAL NEG: " + str(num_neg_seqs))
	num_pos_train=math.ceil(0.8*num_pos_seqs)
	num_pos_valid=num_pos_seqs-num_pos_train
	num_neg_train=math.ceil(0.8*num_neg_seqs)
	num_neg_valid=num_neg_seqs-num_neg_train
	print("POS TRAIN: " + str(num_pos_train))
	print("NEG TRAIN: " + str(num_neg_train))
	print("POS VALID: " + str(num_pos_valid))
	print("NEG VALID: " + str(num_neg_valid))
	createTrainAndValid(posBedFile, negBedFile, posPrefix, negPrefix, num_pos_train, num_neg_train, num_pos_valid, num_neg_valid)

def fillPlaceholders(filename, weightfile, postrain, negtrain, posvalid, negvalid):
	replace(filename, '__BENCHMARKING_WEIGHTFILE', weightfile)
	replace(filename, '__BENCHMARKING_POS_TRAIN', postrain)
	replace(filename, '__BENCHMARKING_NEG_TRAIN', negtrain)
	replace(filename, '__BENCHMARKING_POS_VALID', posvalid)
	replace(filename, '__BENCHMARKING_NEG_VALID', negvalid)

def replace(filename, placeholder, value):
	tmpfilename = filename+".tmp"
        fp=open(filename)
        tmpfp=open(tmpfilename, "w+")
        for line in fp:
                line=line.replace(placeholder, value)
                tmpfp.write(line)
	os.rename(tmpfilename, filename)
        fp.close()

def runMD(md):
	command='(cd ' + md + '; ' + md + '/run_me.sh'+')'
	osutils.runCommandRealTime(command, isShell=True)

#runMD('/users/eprakash/training/momma_dragonn/examples/fasta_sequential_model')
