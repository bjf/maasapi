#!/usr/bin/env python
#

from log                                import center, cleave

# PowerType
#
class PowerType(dict):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, ptype):
        center(s.__class__.__name__)
        s.__maas = maas

        dict.__init__(s, ptype)

        cleave(s.__class__.__name__)

