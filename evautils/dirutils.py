#!/users/eprakash/anaconda2/bin/python

import os
import re
import shutil

def createDir(workingDir, mustcreate=True):
    if not os.path.exists(workingDir):
        os.mkdir(workingDir)
    else:
        if (mustcreate):
            raise ValueError("Directory " + str(workingDir) + " already exists")
        else:
            print("Directory " + str(workingDir) + " already exists")


def copyFileToWorkingDir(f, workingDir):
	os.system('cp ' + f + ' ' + workingDir)

def getFileNameFromPath(path):
	match=re.match('(.*/)*(.*)', path)
	return match.group(2)

def copyDir(dir, destination):
	shutil.copytree(dir, destination, symlinks=True)

#copyDir('/users/eprakash/template/momma_dragonn', '/users/eprakash/temp/training')
