#!/usr/bin/env python
#

from log                                import center, cleave

# Interface
#
class Interface(dict):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, iface):
        center('Interface.__init__')
        s.__maas = maas

        dict.__init__(s, iface)

        cleave('Interface.__init__')

