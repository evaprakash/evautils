#!/users/eprakash/anaconda2/bin/python

import subprocess
import os
import shlex

def runCommandRealTime(command, isShell=False):
	if (isShell):
		process = subprocess.Popen(command,
                          shell=True,
			  stdout=subprocess.PIPE,
			  stderr=subprocess.STDOUT,
                          universal_newlines=True)
	else:
		args=shlex.split(command)
		process = subprocess.Popen(args,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          universal_newlines=True)
	while True:
                output = process.stdout.readline()
                print(output.strip())
                # Do something else
                return_code = process.poll()
                if return_code is not None:
                        print('RETURN CODE:', return_code)
                        # Process has finished, read rest of the output
                        for output in process.stdout.readlines():
                                print(output.strip())
                        break

#command = '/software/homer/default/bin/findMotifs.pl /users/eprakash/bctest/postest.fa fasta /users/eprakash/bctest/H1ESC_400_motifs -fasta /users/eprakash/bctest/matched_no_H1ESC_universal_dnase_400.fa'
#command='ping -c 5 google.com'
#args = shlex.split(command)
#runCommandRealTime(args)
