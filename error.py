# -*- coding: utf-8 -*-
# this module contains a set of custom exceptions
# ref: https://www.programiz.com/python-programming/user-defined-exception
class Error(Exception):
    """Base class for other exceptions"""
    # define the constructure to accept a message
    def __init__(self, msg):
        super(Error, self).__init__(msg)
    pass

class DownloadError(Error):
    
    """raise when nothing download"""
    pass

class InputError(Error):
    
    """raise when typed wrong input"""
    pass
