#!/usr/bin/env python
#

# MapiError
#
class MapiError(Exception):
    '''
    '''
    # __init__
    #
    def __init__(s, reason):
        s.reason = reason

