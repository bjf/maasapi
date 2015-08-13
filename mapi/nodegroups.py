#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from nodegroup                          import Nodegroup
from error                              import MapiError
from power_types                        import PowerTypes

# Nodegroups
#
class Nodegroups(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__nodegroups = None
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
        retval = Nodegroup(s.__maas, s.__nodegroups[index])
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for group in s.__nodegroups:
            n = Nodegroup(s.__maas, group)
            yield n
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__nodegroups is None:
            response = s.__maas._get(u'/nodegroups/', op='list')
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__nodegroups = response.data
            cdebug('    fetched')
        cleave(s.__class__.__name__)

    # power_types
    #
    @property
    def power_types(s):
        center(s.__class__.__name__)

        retval = PowerTypes(s.__maas)

        cleave(s.__class__.__name__)
        return retval
