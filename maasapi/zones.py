#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from error                              import MapiError
from zone                               import Zone
from mydict                             import MyDict

# Zones
#
class Zones(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__zones = None
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
        retval = Zone(s.__maas, s.__zones[index])
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for item in s.__zones:
            n = Zone(s.__maas, item)
            yield n
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__zones is None:
            response = s.__maas.get(u'/zones/')
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__zones = response.data
            cdebug('    fetched')
        cleave(s.__class__.__name__)

    # __setitem__
    #
    def __setitem__(s, key, item):
        center(s.__class__.__name__)
        # item must be a string
        #
        response = s.__maas.post(u'/zones/', data=[('name', key), ('description', item)])
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        s.__zones = None
        cleave(s.__class__.__name__)

    # __delitem__
    #
    def __delitem__(s, key):
        center(s.__class__.__name__)
        response = s.__maas.delete(u'/zones/%s/' % key)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        s.__zones = None
        cleave(s.__class__.__name__)

