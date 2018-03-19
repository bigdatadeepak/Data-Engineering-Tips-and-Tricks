#!/usr/bin/env python
"""
Program Name: Data_Processing.py
Purpose     : Preprocessing files before sending them to Data Lake

        #####################     Change log   ###############################
        ##------------------------------------------------------------------##
        ##  Author              ##Date                ##Current Version     ##
        ##------------------------------------------------------------------##
        ## Deepak               ##20th June,2017      ##V1.0                ##
        ##------------------------------------------------------------------##
        ######################################################################
        Date                Version     Author      Description
        17th July,2017       v 0.1       Deepak     Initial Development
"""

from os import path
from os import makedirs
from os import system
from os import mkdir
from shutil import rmtree
import datetime
import logging
import pysftp
from time import sleep
from os import stat
import os.path as path
import sqlite3
import hashlib

def log_config():
    present_path = path.realpath(__file__)
    log_path = path.join(path.dirname(path.dirname(path.dirname(present_path))), "logs")
    logging.basicConfig(filename=log_path + '\\audit_log.log', level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

#checking for the zero bite file
def zerobytesize(input_file):
    try:
        if not int(stat(input_file).st_size):
            return 1
        else:
            return 0
    except IOError,e:
        print e


def file_duplicacy(file_name,db_path):
    hasher = hashlib.md5()
    with open(file_name, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
        presentfile_id =hasher.hexdigest()

    try:
        db = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row
        with db:
            all_rows = db.execute('''SELECT file_id,file_name FROM audit_table''')
            for row in all_rows:
                fileIds = row['file_id']
                if presentfile_id in fileIds:
                    return 1
                else:
                    try:
                        db = sqlite3.connect(db_path)
                        with db:
                            db.execute('''INSERT INTO audit_table(file_id,file_name)
                                      VALUES(?,?)''', (presentfile_id, file_name))
                    except sqlite3.IntegrityError:
                        print('Record already exists')
                    return 0
    except sqlite3.DatabaseError,e:
        print e

		
def banner(logfile,file_name):
    """
    Purpose: This function will print the "Text" in a banner format

    Args:
        :param action: "Type of Action" you are going to perform
        :param file: "File" on which action is going to be performed

    Returns: None
    """
    output = "|\
            File Under Process: {file} \
            |".format(file = file_name)
    banner = '+'+ '-'*(len(output)-2)+'+'
    boarder = '#'+ ' '*(len(output)-2)+'#' #For 1st and last line space
    style = [banner, boarder, output, boarder, banner]
    design = "\n".join(style)
    with open(logfile,mode= 'a') as ftr:
        ftr.write(design+"\n\n")



if __name__ == "__main__":
    print "Please wait while we executing the code and generate the Log file for you..."
    logpath = path.join(path.dirname(path.dirname(path.realpath(__file__))), "logs\Log_Data_Preprocessing")
    logfile = log_config(logpath, change_log=__doc__)

    #Get all required files
    #Loop Over it for different types of processing:

    #1. Zero Byte File Check
    #2. Duplicate file Check
    banner(logfile, file_name="<File_Name_Variable>")

    #Email client on processing results
    logging.info("Program execution Completed")
    print "Program execution Completed"