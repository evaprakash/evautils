#!/users/eprakash/anaconda2/bin/python

import os
import re
import shutil

def createDir(workingDir):
    if not os.path.exists(workingDir):
        os.mkdir(workingDir)
    else:
        raise ValueError('Directory already exists')

def copyFileToWorkingDir(f, workingDir):
	os.system('cp ' + f + ' ' + workingDir)

def getFileNameFromPath(path):
	match=re.match('(.*/)*(.*)', path)
	return match.group(2)

def copyDir(dir, destination):
	shutil.copytree(dir, destination, symlinks=True)

#copyDir('/users/eprakash/template/momma_dragonn', '/users/eprakash/temp/training')
