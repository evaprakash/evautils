import evautils
import os
from evautils import benchmarkingcontroller
from evautils import dirutils
from evautils import match_gc_content
from evautils import fasta_to_bed
from evautils import osutils
from evautils import sequtils

def generate_benchmarking_sequences(cfg):
    POSITIVE_SEQUENCES_FILE = cfg['DEFAULT']['POSITIVE_SEQUENCES_FILE']
    NEGATIVE_SEQUENCES_FILE = cfg['DEFAULT']['NEGATIVE_SEQUENCES_FILE']
    TARGET_MASTER_DIR = cfg['DEFAULT']['TARGET_MASTER_DIR'] 
    TARGET_SEQUENCES_DIR = TARGET_MASTER_DIR + "/sequences"
    REGION_SIZE = int(cfg['DEFAULT']['REGION_SIZE'])
    CELL_LINE = cfg['DEFAULT']['CELL_LINE']
    GENOME_FILE = cfg['DEFAULT']['GENOME_FILE']
    POS_PREFIX = CELL_LINE +'_' + str(REGION_SIZE)
    NEG_PREFIX = 'universal_dnase_' + str(REGION_SIZE)

    dirutils.createDir(TARGET_MASTER_DIR, mustcreate=False)
    dirutils.createDir(TARGET_SEQUENCES_DIR, mustcreate=False)

    dirutils.copyFileToWorkingDir(POSITIVE_SEQUENCES_FILE, TARGET_SEQUENCES_DIR)
    dirutils.copyFileToWorkingDir(NEGATIVE_SEQUENCES_FILE, TARGET_SEQUENCES_DIR)

    POS_NARROW_PEAKS=TARGET_SEQUENCES_DIR + '/' + dirutils.getFileNameFromPath(POSITIVE_SEQUENCES_FILE)
    NEG_BED_FILE = TARGET_SEQUENCES_DIR + '/' + dirutils.getFileNameFromPath(NEGATIVE_SEQUENCES_FILE)

    posBedFile = TARGET_SEQUENCES_DIR + '/' + POS_PREFIX + '.bed'
    benchmarkingcontroller.narrowPeaksToBed(POS_NARROW_PEAKS, REGION_SIZE, posBedFile)

    noPosNegBedFile = TARGET_SEQUENCES_DIR + '/' + 'no_' + CELL_LINE + '_' + NEG_PREFIX + '.bed'
    benchmarkingcontroller.getExclusiveSets(posBedFile + '.gz', NEG_BED_FILE, noPosNegBedFile)

    posFastaFile = TARGET_SEQUENCES_DIR + '/' + POS_PREFIX + '.fa'
    benchmarkingcontroller.getFasta(GENOME_FILE, posBedFile, posFastaFile)

    negFastaFile = TARGET_SEQUENCES_DIR + '/' + NEG_PREFIX + '.fa'
    benchmarkingcontroller.getFasta(GENOME_FILE, noPosNegBedFile, negFastaFile)

    matchedNegFastaFile = TARGET_SEQUENCES_DIR + '/' + 'matched_' + 'no_' + CELL_LINE + '_' + NEG_PREFIX + '.fa'
    match_gc_content.match_gc_content(posFastaFile, negFastaFile, matchedNegFastaFile, display=False)

    posMotifDir = TARGET_SEQUENCES_DIR + '/' + POS_PREFIX + '_motifs'
    benchmarkingcontroller.runHomer(posFastaFile, matchedNegFastaFile, posMotifDir)

    posMotifMatches = TARGET_SEQUENCES_DIR + '/' + POS_PREFIX + '_motif_matches.txt'
    benchmarkingcontroller.scanMotifGenomeWide(posMotifDir+'/homerMotifs.all.motifs', posFastaFile, posMotifMatches)

    implantedPosFastaFile = TARGET_SEQUENCES_DIR + '/' + 'implanted_' + POS_PREFIX + '.fa'
    benchmarkingcontroller.shuffle_seqs_and_implant_motifs(posFastaFile, posMotifMatches, implantedPosFastaFile)

    implantedPosBedFile = TARGET_SEQUENCES_DIR + '/' + 'implanted_' + POS_PREFIX + '.bed'
    fasta_to_bed.convert(implantedPosFastaFile, implantedPosBedFile)

    matchedNegBedFile = TARGET_SEQUENCES_DIR + '/' + 'matched_' + 'no_' + CELL_LINE + '_' + NEG_PREFIX + '.bed'
    fasta_to_bed.convert(matchedNegFastaFile, matchedNegBedFile)

    os.system('gzip ' + implantedPosBedFile)
    os.system('gzip ' + matchedNegBedFile)
