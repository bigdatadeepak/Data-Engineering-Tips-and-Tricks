"""
This module will do following file validations:
a)	Existance of directory
b)  Zero Byte file check
c)	File Naming Convention
d)	File Layout validation
e)	Duplicate file check
"""

import os.path
import os
import sys
import xml.etree.ElementTree as ET
from glob import glob
import shutil

inputpath = ""
outputpath = ""
errorpath = ""
archivepath = ""
toemail = ""

def xml_read():
    """
    This function will read the xml through ElementTree and retuen the required attribute values
    Argument: xml file path
    return:
    """
    global inputpath,outputpath,errorpath,archivepath,toemail
    xml_file = "config.xml"#sys.argv[1]
    tree = ET.parse(xml_file)
    root = tree.getroot()
    markets = root.findall("market")
    for each_market in markets:
        if each_market.attrib["code"] == "india":
            inputpath = each_market.find("inputpath").text
            outputpath = each_market.find("outputpath").text
            errorpath = each_market.find("errorpath").text
            archivepath = each_market.find("archivepath").text
            toemail = each_market.find("toemail").text
            print("Input Path:{0}\nOutput Path:{1}".format(inputpath,outputpath))

def acknowldge(txt):
    #http://naelshiab.com/tutorial-send-email-python/
    print(txt)

def movefile(source, destination):
    """
    This Function will move file from 'Source dir' to 'Dstination dir'
    param source: Source Directory where the file is prsent
    param destination: Destination directory to which file has to be moved
    return:
    """
    shutil.move(src= source, dst= destination)

def existancecheck():
    global inputpath
    try:
        if (os.path.isdir(str(inputpath))):
            print("Directory exists at the specified path")
        else:
            print("Directory does not exists")
            exit()
    except IOError as a:
        print("Could not check the existance of directory because {}".format(str(a)))

def zerobytefilecheck(inputfile):
    """
    This fuction validated the file for empty content.
    param inputfile: It is the file whose size needs to be checked
    return: Nothing
    """
    if os.stat(inputfile).st_size == 0:
        print("File is Empty.")
        #Moving file to Error Directory
        movefile(source = inputfile, destination = errorpath)
        acknowldge(txt = "File {0} is empty".format(inputfile))
        return 1
    else:
        print("File is ok to continue")
        return 0

def extractdata(inputfile):
    """
    This function will extract the data as per business logic
    param inputfile:
    return: Extracted data if teh data is readable other wise raise the exception
    """
    try:
        print("Data is being processed")
        movefile(source = inputfile, destination = archivepath)
        return 1
    except OSError as e:
        print("Could not process the file because{}".format(str(e)))
        return 0

if __name__ == "__main__":
    xml_read()
    existancecheck()
    #Procesing text files present in the directory
    for file in glob(os.path.join(inputpath,"*.txt")):
        print("Processing starts for file:{0}".format(file))
        status = zerobytefilecheck(inputfile = file)
        if status == 1:
            continue
        status = extractdata(inputfile = file)
        if status == 1:
            acknowldge(txt = "Process of File {0} completed successfully".format(file))
