#!/users/eprakash/anaconda2/bin/python

import subprocess
import os
import shlex

def runCommandRealTime(command, isShell=False, debug=True):
	if (isShell):
		if debug:
			print("Executing command \"" + command + "\"")
		process = subprocess.Popen(command,
                          shell=True,
			  stdout=subprocess.PIPE,
			  stderr=subprocess.STDOUT,
                          universal_newlines=True)
	else:
		args=shlex.split(command)
		if debug:
			print("Executing command \"" + str(args) + "\"")
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

def runCommandCaptureOutput(command, isShell=True, debug=True):
    	if (debug):
		print("Executing command \"" + command + "\"")
	return subprocess.check_output(command, shell=isShell)

def runCommand(command, debug=True):
        if (debug):
                print("Executing command \"" + command + "\"")
        os.system(command)
