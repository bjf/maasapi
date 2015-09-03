#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from error                              import MapiError
from volume_group                       import VolumeGroup

# VolumeGroups
#
class VolumeGroups(object):
    '''
    '''

    # __init__
    #
    def __init__(s, node, system_id):
        center(s.__class__.__name__)
        s.__node = node
        s.__maas = node.client
        s.__system_id = system_id
        s.__groups = None
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
        retval = VolumeGroup().load_dict(s.__groups[index])
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for item in s.__groups:
            n = VolumeGroup().load_dict(item)
            yield n
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__groups is None:
            response = s.__maas.get(u'/nodes/%s/volume-groups/' % s.__system_id)
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__groups = response.data
            cdebug('    fetched')
        cleave(s.__class__.__name__)

