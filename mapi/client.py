#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from restclient                         import RestClient
from nodegroups                         import Nodegroups

# MapiClient
#
class MapiClient(object):
    '''
    '''

    def __init__(s, url, creds):
        center('MapiClient.__init__')
        cdebug('      url: %s' % url)
        cdebug('    creds: %s' % creds)

        s.maas = RestClient(url, creds)

        cleave('MapiClient.__init__')

    @property
    def nodegroups(s):
        return Nodegroups(s.maas)

