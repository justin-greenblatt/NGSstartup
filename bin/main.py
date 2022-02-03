#! /usr/bin/python3
import os
import logging
import settings
from shellTools import shell, aptInstall
from sraInstall import sraInstall

if __name__ == '__main__':
    homePath = os.environ.get("HOME")
    logPath = os.path.join(homePath, "logs") 
    binPath = os.path.join(homePath, "bin")
    dataPath = os.path.join(homePath, "data")
    sumPath = os.path.join(homePath, "summaries")
    for p in [logPath, binPath, dataPath, sumPath]:
        os.mkdir(p)
    
    logging.basicConfig(filename=os.path.join(logPath, 'startup.log'), level=logging.DEBUG)
    os.chdir(homePath)

    shell(["apt", "update"], sudo=True)
    for p in settings.INSTALL_PACKAGES:
        p, aptInstall(p)
    
    os.chdir(binPath)
    execulatblesPath = sraInstall(settings.SRA_TOOLKIT_LINK)