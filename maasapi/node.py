#!/usr/bin/env python
#

from log                                import center, cleave
from mydict                             import MyDict
from error                              import (
                                                 MaasApiHttpServiceUnavailable,
                                                 MaasApiHttpConflict,
                                                 MaasApiPowerResponseTimeout,
                                                 MaasApiNotImplemented,
                                                 MaasApiNodeStateReady,
                                               )
from volume_groups                      import VolumeGroups

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
    def client(s):
        '''
        '''
        return s.__maas

    @property
    def power_state(s):
        '''
        '''
        center(s.__class__.__name__)
        try:
            response = s.__maas.get(u'/nodes/%s/' % s['system_id'], op='query_power_state')
            retval = response.data['state']
        except MaasApiHttpServiceUnavailable as e:
            raise MaasApiPowerResponseTimeout(e.status, e.message)
        cleave(s.__class__.__name__)
        return retval

    @property
    def power_parameters(s):
        '''
        '''
        center(s.__class__.__name__)
        try:
            response = s.__maas.get(u'/nodes/%s/' % s['system_id'], op='power_parameters')
            retval = response.data
        except MaasApiHttpServiceUnavailable as e:
            raise MaasApiPowerResponseTimeout(e.status, e.message)
        cleave(s.__class__.__name__)
        return retval

    def abort(s):
        '''
        '''
        center(s.__class__.__name__)
        try:
            response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='abort_operation')
            retval = response.data
        except MaasApiHttpConflict as e:
            raise MaasApiPowerResponseTimeout(e.status, e.message)
        cleave(s.__class__.__name__)

    @property
    def details(s):
        '''
        '''
        center(s.__class__.__name__)
        response = s.__maas.get(u'/nodes/%s/' % s['system_id'], op='details')
        retval = response.data
        cleave(s.__class__.__name__)
        return retval

    def abort_operation(s):
        '''
        '''
        response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='abort_operation')
        return response

    def clain_sticky_ip_address(s, mac_address=None, requested_address=None):
        '''
        '''
        data = []
        if mac_address:
            data.append( ('mac_address', mac_address) )
        if requested_address:
            data.append( ('requested_address', requested_address) )
        response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='claim_sticky_ip_address', data=data)
        return response

    def commission(s):
        response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='commission')
        raise MaasApiNotImplemented()

    def mark_broken(s, description=None):
        response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='mark_broken')
        raise MaasApiNotImplemented()

    def release(s):
        response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='release')
        raise MaasApiNotImplemented()

    def set_storage_layout(s):
        raise MaasApiNotImplemented()

    def start(s, distro_series=None, hwe_kernel=None, user_data=None):
        response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='start')
        raise MaasApiNotImplemented()

    def stop(s, mode=None):
        response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='stop')
        raise MaasApiNotImplemented()

    @property
    def volume_groups(s):
        return VolumeGroups(s, s['system_id'])

    @volume_groups.setter
    def volue_groups(s, vgroups):
        pass
