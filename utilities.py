'''
File Name      : utility_tools.py
Author Name    : Lakshmi Damodara
Date           : 03/02/2018
Version        : 1.0
Description    : This program is for all general purpose tools

'''

import sys
import inspect

def __LINE__():
    return sys.exc_info()[2].tb_frame.f_back.f_lineno

def __FILE__():
    return inspect.currentframe().f_code.co_filename


#User Defined exception Handling
class DLException(Exception):
    def __init__(self, filename, lineno, errstr = None):
        if errstr is None:
            errstr = "An exception occured"
        self.value = errstr
        self.name = filename
        self.line = lineno
    def __str__(self):
        return str("%s in %s at lineNo %d" %(self.value, self.name, self.line) )

