import os
import evautils
from evautils import mommadragonnutils
from evautils import dirutils
from evautils import osutils
from evautils import match_gc_content

def train_momma_dragonn(cfg):
    TARGET_MASTER_DIR = cfg['DEFAULT']['TARGET_MASTER_DIR'] 
    TARGET_SEQUENCES_DIR = TARGET_MASTER_DIR + "/sequences"
    TARGET_TRAINING_DIR = TARGET_MASTER_DIR + "/training"
    REGION_SIZE = int(cfg['DEFAULT']['REGION_SIZE'])
    CELL_LINE = cfg['DEFAULT']['CELL_LINE']
    MOMMA_DRAGONN_TEMPLATE_DIR=cfg['DEFAULT']['MOMMA_DRAGONN_TEMPLATE_DIR']
    PRE_TRAINED_MODEL_WEIGHTS=cfg['DEFAULT']['PRE_TRAINED_MODEL_WEIGHTS']
    POS_PREFIX = CELL_LINE +'_' + str(REGION_SIZE)
    NEG_PREFIX = 'universal_dnase_' + str(REGION_SIZE)
    IMPLANTED_POS_BED_FILE = TARGET_SEQUENCES_DIR + '/implanted_' + POS_PREFIX + '.bed.gz'
    MATCHED_NEG_BED_FILE = TARGET_SEQUENCES_DIR + '/matched_no_' + CELL_LINE + '_' + NEG_PREFIX + '.bed.gz'
    MOMMA_DRAGONN=TARGET_TRAINING_DIR+'/'+'momma_dragonn'

    dirutils.createDir(TARGET_MASTER_DIR, mustcreate=False)
    dirutils.createDir(TARGET_TRAINING_DIR, mustcreate=False)
    dirutils.copyDir(MOMMA_DRAGONN_TEMPLATE_DIR, MOMMA_DRAGONN)
    os.system('cp ' + PRE_TRAINED_MODEL_WEIGHTS + ' ' + TARGET_TRAINING_DIR)

    mommadragonnutils.splitDatasets(IMPLANTED_POS_BED_FILE, MATCHED_NEG_BED_FILE, TARGET_TRAINING_DIR+'/'+POS_PREFIX, TARGET_TRAINING_DIR+'/'+NEG_PREFIX)
    match_gc_content.gc_sanity_check(TARGET_TRAINING_DIR+'/'+POS_PREFIX+'_train.bed.gz', TARGET_TRAINING_DIR+'/'+NEG_PREFIX+'_train.bed.gz', display=False)
    match_gc_content.gc_sanity_check(TARGET_TRAINING_DIR+'/'+POS_PREFIX+'_valid.bed.gz', TARGET_TRAINING_DIR+'/'+NEG_PREFIX+'_valid.bed.gz', display=False)

    mommadragonnutils.fillPlaceholders(MOMMA_DRAGONN+'/examples/fasta_sequential_model/config/hyperparameter_configs_list.yaml', PRE_TRAINED_MODEL_WEIGHTS, TARGET_TRAINING_DIR+'/'+POS_PREFIX+'_train.bed.gz', TARGET_TRAINING_DIR+'/'+NEG_PREFIX+'_train.bed.gz', TARGET_TRAINING_DIR+'/'+POS_PREFIX+'_valid.bed.gz', TARGET_TRAINING_DIR+'/'+NEG_PREFIX+'_valid.bed.gz')
    mommadragonnutils.fillPlaceholders(MOMMA_DRAGONN+'/examples/fasta_sequential_model/config/valid_data_loader_config.yaml', PRE_TRAINED_MODEL_WEIGHTS, TARGET_TRAINING_DIR+'/'+POS_PREFIX+'_train.bed.gz', TARGET_TRAINING_DIR+'/'+NEG_PREFIX+'_train.bed.gz', TARGET_TRAINING_DIR+'/'+POS_PREFIX+'_valid.bed.gz', TARGET_TRAINING_DIR+'/'+NEG_PREFIX+'_valid.bed.gz')

    md=MOMMA_DRAGONN+'/examples/fasta_sequential_model'
    mommadragonnutils.runMD(md)
