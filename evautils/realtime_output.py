#!/users/eprakash/anaconda2/bin/python

import os
import subprocess

def runCommand(commandList):
	process = subprocess.Popen(commandList, 
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

runCommand(['ping', '-c 4', 'python.org'])
