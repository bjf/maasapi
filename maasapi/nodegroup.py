#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from interfaces                         import Interfaces
from boot_images                        import BootImages
from error                              import MapiError
import bson
import json

# Nodegroup
#
class Nodegroup(dict):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, group):
        center('Nodegroup.__init__')
        s.__maas   = maas
        cdebug('group: %s' % group)

        dict.__init__(s, group)

        cleave('Nodegroup.__init__')

    # interfaces
    #
    @property
    def interfaces(s):
        '''
        A collection of all of the network interfaces for a particular nodegroup.
        '''
        center('Nodegroup.interfaces')

        retval = Interfaces(s.__maas, s['uuid'])

        center('Nodegroup.interfaces')
        return retval

    # boot_images
    #
    @property
    def boot_images(s):
        '''
        A collection of all of the boot imags for a particular nodegroup.
        '''
        center(s.__class__.__name__)

        retval = BootImages(s.__maas, s['uuid'])

        cleave(s.__class__.__name__)
        return retval

    # nodes
    #
    @property
    def nodes(s):
        '''
        A collection of all of the nodes in a particular nodegroup.
        '''
        center(s.__class__.__name__)

        # Will probably produce a Nodes object but for now just return what comes
        # back from the rest interface.
        #
        response = s.__maas.get(u'/nodegroups/%s/' % s['uuid'], op='list_nodes')
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)

        retval = response.data

        cleave(s.__class__.__name__)
        return retval

    # details
    #
    @property
    def details(s):
        '''
        A collection of detailed information about all of the nodes
        in a particular nodegroup.
        '''
        center(s.__class__.__name__)

        #from client                             import MCA

        # Will probably produce a Nodes object but for now just return what comes
        # back from the rest interface.
        #
        response = s.__maas.post(u'/nodegroups/%s/' % s['uuid'], op='details')
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)

        data = bson.BSON.decode(response.data)
        cdebug(json.dumps(data, sort_keys=True, indent=4))

        retval = response.data

        cleave(s.__class__.__name__)
        return retval

    # import_boot_images
    #
    def import_boot_images(s):
        '''
        Import the boot image files for a particular nodegroup.
        '''
        center(s.__class__.__name__)

        # Will probably produce a Nodes object but for now just return what comes
        # back from the rest interface.
        #
        response = s.__maas.post(u'/nodegroups/%s/' % s['uuid'], op='import_boot_images')
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)

        retval = response.data

        cleave(s.__class__.__name__)
        return retval

