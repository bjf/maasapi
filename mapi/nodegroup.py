#!/usr/bin/env python
#

from log                                import center, cleave

# Nodegroup
#
class Nodegroup(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, group):
        center('Nodegroup.__init__')
        s.__maas = maas
        s.__group = group
        for k in group:
            setattr(s, k, group[k])
        cleave('Nodegroup.__init__')

