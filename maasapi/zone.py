#!/usr/bin/env python
#

from log                                import center, cleave
from mydict                             import MyDict

# Zone
#
class Zone(MyDict):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, obj):
        center(s.__class__.__name__)
        s.__maas = maas

        dict.__init__(s, obj)

        cleave(s.__class__.__name__)

