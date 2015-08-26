#
# Copyright 2015, Canonical Ltd
#

class Response(object):
    """
    Response for the API calls to use internally
    """
    def __init__(self, ok=False, data=None):
        self.ok = ok
        self.data = data

