#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from error                              import MapiError
from event                              import Event

# Events
#
class Events(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__prev_uri = None
        s.__next_uri = None
        s.__count = 0
        s.__events = None
        s.__item_index = 0
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
        print(index)
        retval = Event(s.__maas, s.__events[index])
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for item in s.__events:
            s.__item_index += 1
            n = Event(s.__maas, item)
            yield n
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__events is None:
            response = s.__maas.get(u'/events/', op='query')
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__prev_uri = response.data['prev_uri']
            s.__next_uri = response.data['next_uri']
            s.__count  = response.data['count']
            s.__events = response.data['events']
            cdebug('    fetched')
        cleave(s.__class__.__name__)

