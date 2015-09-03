#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from error                              import MapiError
from node                               import Node

# Nodes
#
class Nodes(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, op='list', uri=u'/nodes/'):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__resources = None
        s.__op = op
        s.__uri = uri
        cleave(s.__class__.__name__)

    # __len__
    #
    def __len__(s):
        return len(list(s.__iter__()))

    # __getitem__
    #
    def __getitem__(s, index):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        retval = Node(s.__maas, s.__resources[index])
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for group in s.__resources:
            n = Node(s.__maas, group)
            yield n
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__resources is None:
            response = s.__maas.get(s.__uri, op=s.__op)
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__resources = response.data
            cdebug('    fetched')
        cleave(s.__class__.__name__)

