from subprocess import Popen, PIPE
import os
import logging
import requests
import shutil


#Download styff from the internet into the current working directory
def downloadFromURL(url, filename = False):
    if not filename:
        filename = url.split('/')[-1]
    h = open(filename, 'wb+')
    r = requests.get(url, stream=True, allow_redirects=True)
    h.write(r.content)
    return 0


#General shell command with logging
def shell(command, sudo = True, message = "", script = False, getOutput = False):

    if sudo:
        command.insert(0, "sudo")
    p = Popen(command,
                  stdout=PIPE,
                  stderr=PIPE,
                  shell = script)
    p.wait()
    o,e = p.communicate()
    if p.returncode:
        logging.error("{}${}\nSTDERR{}".format(message, " ".join(p.args), e))
    else:
        logging.debug("{}${}\nSTDIN{}".format(message, " ".join(p.args), o))

    if getOutput:
        return o
    else:    
        return p.returncode

#Give name of package 
def aptInstall(package):
    command = ["apt", "install", "-y", package]
    return shell(command, sudo=True, message = "Installing {} with apt".format(package))

#Extract tar files
def tarExtract(inFilePath):
    return shell(["tar", "-xf", inFilePath], sudo = True)

#Use fastqdump to download stuff
def fastqdump(srr):
    command = ["fastq-dump",  srr]
    return shell(command, sudo = True, message = "Getting {} with fastq-dump".format(srr))

#making a file executable
def makeFileExecutable(path):
    if os.path.isfile(path):
        p = shell(["readlink", "-f", path])
        return shell(["chmod", "777", p], sudo = True)
    else:
        return 0

#Make file executable from anywhere by adding to PATH variable
def addToPATH(pathToAdd):
    return shell(["PATH=$PATH:" + pathToAdd], sudo = False, script = True)
