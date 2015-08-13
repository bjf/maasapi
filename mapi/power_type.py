#!/usr/bin/env python
#

from log                                import center, cleave
from copy                               import deepcopy

# PowerType
#
class PowerType(dict):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, ptype):
        center('PowerType.__init__')
        s.__maas = maas

        dict.__init__(s, ptype)

        cleave('PowerType.__init__')

