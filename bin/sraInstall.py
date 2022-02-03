from subprocess import Popen, PIPE
import os
import logging
from shellTools import downloadFromURL, tarExtract, makeFileExecutable, addToPATH, shell
from time import sleep

#Downloads and installs sratoolkit for google Cloud VMs
def sraInstall(l):
    
    #declaring paths
    compressedFile = os.path.join(os.getcwd(), l.split('/')[-1])
    decompressedFile = compressedFile.rstrip(".tar.gz")
    executablesFolder = os.path.join(decompressedFile, "bin")
    executableFile = os.path.join(executablesFolder, "fastq-dump")

    #getting link
    downloadFromURL(l)
    
    #extracting
    tarExtract(compressedFile)
    
    #making executable    
    #makeFileExecutable(executableFile)
    #for e in os.listdir(executablesFolder):
    #    makeFileExecutable(os.path.join(executablesFolder, e))
    
    #Adding folder to path
    addToPATH(executablesFolder)  

    #sratoolkit setup for cloud VM
    shell([os.path.join(executablesFolder, "vdb-config"), "--report-cloud-identity", "yes"], sudo = False)
    shell([os.path.join(executablesFolder, "vdb-config"), "--accept-gcp-charges", "yes"], sudo = False)
    #anoying necessity to utilize the vdb-config interractive mode.
    #opening and closing it in the background will work to get around this.
    i = Popen(["nohup", os.path.join(executablesFolder, "vdb-config"), "--interactive"], stdin=PIPE)
    i.communicate("x\n".encode('utf-8'))
    sleep(0.5)
    i.kill()
    shell(["PATH=$PATH:" + executablesFolder], script = True, sudo = False)
    return executableFile
