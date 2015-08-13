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
        center('PowerTypes.__init__')
        s.__maas = maas
        s.__power_types = None
        cleave('PowerTypes.__init__')

    # __len__
    #
    def __len__(s):
        return len(list(s.__iter__()))

    # __getitem__
    #
    def __getitem__(s, index):
        center('PowerTypes.__getitem__')
        s.__fetch_if_needed()
        retval = PowerType(s.__maas, s.__power_types[index])
        cleave('PowerTypes.__getitem__')
        return retval

    # __iter__
    #
    def __iter__(s):
        center('PowerTypes.__iter__')
        s.__fetch_if_needed()
        for ptype in s.__power_types:
            n = PowerType(s.__maas, ptype)
            yield n
        cleave('PowerTypes.__iter__')

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center('PowerTypes.__fetch_if_needed')
        if s.__power_types is None:
            response = s.__maas._get(u'/nodegroups/', op='describe_power_types')
            if not response.ok:
                if type(response.data) == str:
                    cleave('PowerTypes.__fetch_if_needed')
                    raise MapiError(response.data)

            s.__power_types = response.data
            cdebug('    fetched')
        cleave('PowerTypes.__fetch_if_needed')

