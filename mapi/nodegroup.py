#!/usr/bin/env python
#

from log                                import center, cleave
from interfaces                         import Interfaces
from boot_images                        import BootImages

# Nodegroup
#
class Nodegroup(dict):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, group):
        center('Nodegroup.__init__')
        s.__maas = maas

        dict.__init__(s, group)

        cleave('Nodegroup.__init__')

    # interfaces
    #
    @property
    def interfaces(s):
        center('Nodegroup.interfaces')

        retval = Interfaces(s.__maas, s['uuid'])

        center('Nodegroup.interfaces')
        return retval

    # boot_images
    #
    @property
    def boot_images(s):
        center(s.__class__.__name__)

        retval = BootImages(s.__maas, s['uuid'])

        cleave(s.__class__.__name__)
        return retval
