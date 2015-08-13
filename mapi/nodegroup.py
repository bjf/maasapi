#!/usr/bin/env python
#

from log                                import center, cleave
from copy                               import deepcopy

# Nodegroup
#
class Nodegroup(dict):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, group):
        center('Nodegroup.__init__')
        s.__maas = maas

        dict.__init__(s, group)

        cleave('Nodegroup.__init__')

    # interfaces
    #
    @property
    def interfaces(s):
        center('Nodegroup.interfaces')

        # nodegroups interfaces ---
        _url = u'/nodegroups/%s/interfaces/' % s['uuid']
        response = s.__maas._get(_url, op='list')
        retval = response.data

        center('Nodegroup.interfaces')
        return retval

