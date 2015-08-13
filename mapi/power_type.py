#!/usr/bin/env python
#

from log                                import center, cleave
from copy                               import deepcopy

# PowerType
#
class PowerType(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, ptype):
        center('PowerType.__init__')
        s.__maas = maas
        s.__power_type = ptype

        s._dict = dict()
        s._dict = deepcopy(ptype)
        cleave('PowerType.__init__')

    # __len__
    #
    def __len__(s):
        return len(list(s._dict.__iter__()))

    # __getitem__
    #
    def __getitem__(s, index):
        center('PowerType.__getitem__')
        retval = s._dict[index]
        cleave('PowerType.__getitem__')
        return retval

    # __iter__
    #
    def __iter__(s):
        center('PowerType.__iter__')
        retval = s._dict.__iter__()
        cleave('PowerType.__iter__')

    # __str__
    #
    def __str__(s):
        return str(s._dict)
