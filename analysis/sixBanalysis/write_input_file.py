"""
This script will populate a text file with all ROOT files available in a given CRAB output directory.
"""

from argparse import ArgumentParser
# from icecream import ic
import os
import subprocess

parser = ArgumentParser(description='Command line parser of model options and tags')
parser.add_argument('--dir', dest = 'dir', help = 'CRAB output directory' , required = True)
args = parser.parse_args()

dirName = args.dir

def exists_on_eos(lfn):
    """ check if lfn (starting with /store/group) exists """
    retcode = os.system('eos root://cmseos.fnal.gov ls -s %s > /dev/null 2>&1' % lfn)
    # print "THE FOLDER", lfn, "RETURNED CODE", retcode
    return True if retcode == 0 else False

with open("fileList.txt", "w") as f:
    if (exists_on_eos(dirName)):
        output = subprocess.run(["eos", "root://cmseos.fnal.gov", "ls", dirName], capture_output=True)
        listOfDirs = output.stdout.decode("utf-8").split("\n")
        for eachDir in listOfDirs:
            if eachDir != '':
                fullPath = dirName + eachDir
                output = subprocess.run(["eos", "root://cmseos.fnal.gov", "ls", fullPath], capture_output=True)
                listOfFiles = output.stdout.decode("utf-8").split("\n")
                for fileName in listOfFiles:
                    if fileName != '':
                        f.write("root://cmseos.fnal.gov/" + fullPath + '/' + fileName + '\n')
    else:
        print("Failed to write.")

# # ic(dirName)
# print(os.stat(dirName))

# if os.path.isdir(dirName):
#     dirList = os.listdir(dirName)
#     print(dirList)
#     for subDir in dirList:
#         fileList = os.listdir(subDir)
#         print(fileList[:10])
# else:
#     print("Input must be a valid directory!")
#     raise