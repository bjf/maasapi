#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from restclient                         import RestClient
from nodegroups                         import Nodegroups

# MAASClient
#
class MAASClient(object):
    '''
    '''

    def __init__(s, url, creds):
        center('MAASClient.__init__')
        cdebug('      url: %s' % url)
        cdebug('    creds: %s' % creds)

        s.maas = RestClient(url, creds)

        cleave('MAASClient.__init__')

    @property
    def nodegroups(s):
        return Nodegroups(s.maas)

