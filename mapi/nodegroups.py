#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from nodegroup                          import Nodegroup

# Nodegroups
#
class Nodegroups(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas):
        center('Nodegroups.__init__')
        s.__maas = maas
        s.__nodegroups = None
        cleave('Nodegroups.__init__')

    # __len__
    #
    def __len__(s):
        return len(list(s.__iter__()))

    # __getitem__
    #
    def __getitem__(s, index):
        center('Nodegroups.__getitem__')
        s.__fetch_if_needed()
        retval = Nodegroup(s.__maas, s.__nodegroups[index])
        cleave('Nodegroups.__getitem__')
        return retval

    # __iter__
    #
    def __iter__(s):
        center('Nodegroups.__iter__')
        s.__fetch_if_needed()
        for group in s.__nodegroups:
            n = Nodegroup(s.__maas, group)
            yield n
        cleave('Nodegroups.__iter__')

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center('Nodegroups.__fetch_if_needed')
        if s.__nodegroups is None:
            response = s.__maas._get(u'/nodegroups/', op='list')
            s.__nodegroups = response.data
            cdebug('    fetched')
        cleave('Nodegroups.__fetch_if_needed')

