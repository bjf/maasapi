#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from boot_image                         import BootImage
from error                              import MapiError

# BootImages
#
class BootImages(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, uuid):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__uuid = uuid
        s.__boot_images = None
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
        retval = BootImage(s.__maas, s.__boot_images[index])
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for ptype in s.__boot_images:
            n = BootImage(s.__maas, ptype)
            yield n
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__boot_images is None:
            response = s.__maas.get(u'/nodegroups/%s/boot-images/' % s.__uuid)
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__boot_images = response.data
            cdebug('    fetched')
        cleave(s.__class__.__name__)

