#!/usr/bin/env python
#

from log                                import center, cleave

# BootSource
#
class BootSource(dict):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, image):
        center(s.__class__.__name__)
        s.__maas = maas

        dict.__init__(s, image)

        cleave(s.__class__.__name__)

