#!/usr/bin/env python
#

from log                                import center, cleave
from mydict                             import MyDict
from error                              import MapiError

# Node
#
class Node(MyDict):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, obj):
        center(s.__class__.__name__)
        s.__maas = maas

        dict.__init__(s, obj)

        cleave(s.__class__.__name__)

    @property
    def power_state(s):
        center(s.__class__.__name__)
        response = s.__maas.get(u'/nodes/%s/' % s['system_id'], op='query_power_state')
        retval = response.data['state']
        cleave(s.__class__.__name__)
        return retval
