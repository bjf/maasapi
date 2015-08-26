#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from power_type                         import PowerType
from error                              import MapiError

# PowerTypes
#
class PowerTypes(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__power_types = None
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
        retval = PowerType(s.__maas, s.__power_types[index])
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for ptype in s.__power_types:
            n = PowerType(s.__maas, ptype)
            yield n
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__power_types is None:
            response = s.__maas.get(u'/nodegroups/', op='describe_power_types')
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__power_types = response.data
            cdebug('    fetched')
        cleave(s.__class__.__name__)

