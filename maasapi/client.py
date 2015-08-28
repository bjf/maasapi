#!/usr/bin/env python
#


from log                                import center, cleave, cdebug
from restclient                         import RestClient

from nodegroups                         import Nodegroups
from boot_resources                     import BootResources
from boot_sources                       import BootSources
from nodes                              import Nodes
from zones                              import Zones

# MapiClient
#
class MapiClient(RestClient):
    '''
    '''

    def __init__(s, url, creds):
        center(s.__class__.__name__)
        cdebug('      url: %s' % url)
        cdebug('    creds: %s' % creds)
        super(MapiClient, s).__init__(url, creds)
        cleave(s.__class__.__name__)

    @property
    def nodegroups(s):
        return Nodegroups(s)

    @property
    def boot_resources(s):
        return BootResources(s)

    @property
    def boot_sources(s):
        return BootSources(s)

    @property
    def nodes(s):
        return Nodes(s)

    @property
    def zones(s):
        return Zones(s)

    @property
    def nodes_allocated(s):
        return Nodes(s, op='list_allocated')

    def post(s, uri, op=None, data=[]):
        center(s.__class__.__name__)
        response = s.call(u'%s/%s' % (s.root, uri), op=op, data=data, method='POST', creds=s.creds)
        cleave(s.__class__.__name__)
        return response

    def get(s, uri, op=None, data=[]):
        center(s.__class__.__name__)
        response = s.call(u'%s/%s' % (s.root, uri), op=op, data=data, method='GET', creds=s.creds)
        cleave(s.__class__.__name__)
        return response

    def delete(s, uri, op=None, data=[]):
        center(s.__class__.__name__)
        response = s.call(u'%s/%s' % (s.root, uri), op=op, data=data, method='DELETE', creds=s.creds)
        cleave(s.__class__.__name__)
        return response

