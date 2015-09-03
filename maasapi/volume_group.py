#!/usr/bin/env python
#

from log                                import center, cleave

# VolumeGroup
#
class VolumeGroup(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, name=None, uuid=None, block_devices=None, partitions=None):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__name          = name
        s.__uuid          = uuid
        s.__block_devices = block_devices
        s.__partitions    = partitions
        cleave(s.__class__.__name__)

    @property
    def name(s):
        return s.__name

    @property
    def uuid(s):
        return s.__uuid

    @property
    def block_devices(s):
        return s.__block_devices

    @property
    def partitions(s):
        return s.__partitions

    def load_dict(s, d):
        s.__name          = d.get('name', None)
        s.__uuid          = d.get('uuid', None)
        s.__block_devices = d.get('block_devices', None)
        s.__partitions    = d.get('partitions', False)
        return s

    def to_rest_data(s):
        retval = []
        retval.append(('name', s.__name))
        retval.append(('uuid', s.__uuid))
        retval.append(('block_devices', s.__block_devices))
        retval.append(('partitions', s.__partitions))
        return retval
