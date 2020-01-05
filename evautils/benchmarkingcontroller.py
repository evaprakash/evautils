#!/users/eprakash/anaconda2/bin/python

import os
import gzip
import re
import subprocess
import evautils
from evautils import osutils
from evautils import shuffle_sequences_add_motifs

def runCommandRealTime(command):
        print(command)
	process = subprocess.Popen(command,
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
        while True:
                output = process.stdout.readline()
                print(output.strip())
                # Do something else
                return_code = process.poll()
                if return_code is not None:
                        print('RETURN CODE', return_code)
                        # Process has finished, read rest of the output
                        for output in process.stdout.readlines():
                                print(output.strip())
                        break


def narrowPeaksToBed(narrowPeaksFile, regionSize, bedfile):
        fp_np = gzip.open(narrowPeaksFile)
        fp_bed = open(bedfile, 'w')
        for line in fp_np:
                match = re.match("(\S+)\s+(\d+)\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\d+)\s*$", line)
                if match:
                        chrom = match.group(1)
                        chromStart = int(match.group(2))
                        chromSummitOffset = int(match.group(3))
                        regionStart = chromStart + chromSummitOffset - int(regionSize/2)
                        regionEnd = regionStart + regionSize
                        fp_bed.write(chrom + "\t" + str(regionStart) + "\t" + str(regionEnd) + "\n")
        fp_np.close()
        fp_bed.close()
        cmd = 'gzip ' + bedfile
        os.system(cmd)

def getExclusiveSets(posBedFile, negBedFile, noPosNegBedFile):
        cmd = 'intersectBed -v -a ' + negBedFile + ' -b '+ posBedFile + ' -wa | gzip -c > ' + noPosNegBedFile
	os.system(cmd)

def getFasta(genomeFile, bedFile, fastaFile):
	os.system('gunzip ' + bedFile)
	cmd = 'bedtools getfasta -fi ' + genomeFile + ' -bed '+ bedFile + ' > ' + fastaFile + ' 2> errors.txt'
	os.system(cmd)
	os.system('gzip ' + bedFile)

def runHomer(fastaFile, bgFastaFile, motifDir):
	cmd = '/software/homer/default/bin/findMotifs.pl ' + fastaFile + ' fasta ' + motifDir + ' -fasta ' +  bgFastaFile
	osutils.runCommandRealTime(cmd)

def scanMotifGenomeWide(allMotifsFile, fastaFile, motifMatchesFile):
        cmd = '/software/homer/default/bin/scanMotifGenomeWide.pl ' + allMotifsFile + ' ' + fastaFile + ' > ' + motifMatchesFile
        osutils.runCommandRealTime(cmd, isShell=True)

def shuffle_seqs_and_implant_motifs(sequenceFile, motifMatchesFile, implantedFile):
	shuffle_sequences_add_motifs.shuffle_sequences_add_motifs(sequenceFile, motifMatchesFile, implantedFile)
