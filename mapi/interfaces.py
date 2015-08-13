#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from interface                          import Interface
from error                              import MapiError

# Interfaces
#
class Interfaces(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, uuid):
        center('Interfaces.__init__')
        s.__maas = maas
        s.__uuid = uuid
        s.__interfaces = None
        cleave('Interfaces.__init__')

    # __len__
    #
    def __len__(s):
        return len(list(s.__iter__()))

    # __getitem__
    #
    def __getitem__(s, index):
        center('Interfaces.__getitem__')
        s.__fetch_if_needed()
        retval = Interface(s.__maas, s.__interfaces[index])
        cleave('Interfaces.__getitem__')
        return retval

    # __iter__
    #
    def __iter__(s):
        center('Interfaces.__iter__')
        s.__fetch_if_needed()
        for iface in s.__interfaces:
            n = Interface(s.__maas, iface)
            yield n
        cleave('Interfaces.__iter__')

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center('Interfaces.__fetch_if_needed')
        if s.__interfaces is None:
            response = s.__maas._get(u'/nodegroups/%s/interfaces/' % s.__uuid, op='list')
            if not response.ok:
                if type(response.data) == str:
                    cleave('Interfaces.__fetch_if_needed')
                    raise MapiError(response.data)

            s.__interfaces = response.data
            cdebug('    fetched')
        cleave('Interfaces.__fetch_if_needed')

