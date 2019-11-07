# -*- coding: utf-8 -*-
# this module contains a set of custom exceptions
# ref: https://julien.danjou.info/python-exceptions-guide/
class Error(Exception):
    """Base class for other exceptions"""
    def __init__(self, msg):
        super(Error, self).__init__(msg)
    pass

class DownloadError(Error):
    
    """raise when nothing download"""
    pass


