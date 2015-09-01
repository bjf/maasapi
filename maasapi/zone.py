#!/usr/bin/env python
#

from log                                import center, cleave

# Zone
#
class Zone(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, obj):
        center(s.__class__.__name__)
        s.__maas = maas

        s.__name         = obj['name']
        s.__description  = obj['description']
        s.__resource_uri = obj['resource_uri']

        cleave(s.__class__.__name__)

    @property
    def name(s):
        return s.__name

    @property
    def description(s):
        return s.__description

    @property
    def resource_uri(s):
        return s.__resource_uri

