#!/usr/bin/env python
#

from log                                import center, cleave
from mydict                             import MyDict
from error                              import (
                                                 MaasApiHttpServiceUnavailable,
                                                 MaasApiHttpConflict,
                                                 MaasApiHttpBadRequest,
                                                 MaasApiHttpInternalServerError,
                                                 MaasApiPowerResponseTimeout,
                                                 MaasApiNotImplemented,
                                                 MaasApiNodeStateReady,
                                                 MaasApiNodeNotAcquired,
                                                 MaasApiNodeAlreadyAcquired,
                                                 MaasApiNodeBadMACAddress,
                                                 MaasApiDHCPServerDisabled,
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
            raise MaasApiNodeStateReady(e.status, e.message)
        cleave(s.__class__.__name__)

    def commission(s):
        '''
        '''
        center(s.__class__.__name__)
        try:
            response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='commission')
            retval = Node(s.__maas, response.data)
        except MaasApiHttpConflict as e:
            raise MaasApiPowerResponseTimeout(e.status, e.message)
        cleave(s.__class__.__name__)
        return retval

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
        center(s.__class__.__name__)
        response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='abort_operation')
        return response

    def claim_sticky_ip_address(s, mac_address=None, requested_address=None):
        '''
        '''
        center(s.__class__.__name__)
        data = []
        if mac_address:
            data.append( ('mac_address', mac_address) )
        if requested_address:
            data.append( ('requested_address', requested_address) )
        try:
            response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='claim_sticky_ip_address', data=data)
            retval = response.data
        except MaasApiHttpBadRequest as e:
            raise MaasApiNodeBadMACAddress(e.status, e.message)
        except MaasApiHttpInternalServerError as e:
            raise MaasApiDHCPServerDisabled(e.status, e.message)
        cleave(s.__class__.__name__)
        return retval

    def rlease_sticky_ip_address(s, address=None):
        '''
        '''
        center(s.__class__.__name__)
        data = []
        if address:
            data.append( ('address', address) )
        response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='release_sticky_ip_address', data=data)
        retval = response.data
        cleave(s.__class__.__name__)
        return retval

    def _op(s, uri, op=None, data=[]):
        center(s.__class__.__name__)
        response = s.__maas.post(uri, op=op, data=data)
        retval = Node(s.__maas, response.data)
        cleave(s.__class__.__name__)
        return retval

    def mark_broken(s, description=None):
        center(s.__class__.__name__)
        data = []
        if description:
            data.append( ('description', description) )
        retval = s._op(u'/nodes/%s/' % s['system_id'], op='mark_broken', data=data)
        cleave(s.__class__.__name__)
        return retval

    def mark_fixed(s):
        center(s.__class__.__name__)
        retval = s._op(u'/nodes/%s/' % s['system_id'], op='mark_fixed')
        cleave(s.__class__.__name__)
        return retval

    def acquire(s):
        '''
        '''
        center(s.__class__.__name__)
        data = []
        data.append( ('name', s['hostname']) )
        try:
            retval = s._op(u'/nodes/', op='acquire', data=data)
        except MaasApiHttpConflict as e:
            raise MaasApiNodeAlreadyAcquired(e.status, e.message)
        cleave(s.__class__.__name__)
        return retval

    def release(s):
        center(s.__class__.__name__)
        retval = s._op(u'/nodes/%s/' % s['system_id'], op='release')
        cleave(s.__class__.__name__)
        return retval

    def set_storage_layout(s):
        raise MaasApiNotImplemented()

    def start(s, distro_series=None, hwe_kernel=None, user_data=None):
        '''
        '''
        center(s.__class__.__name__)
        data = []
        if distro_series:
            data.append( ('distro_series', distro_series) )
        if hwe_kernel:
            data.append( ('hwe_kernel', hwe_kernel) )
        if user_data:
            data.append( ('user_data', user_data) )
        try:
            retval = s._op(u'/nodes/%s/' % s['system_id'], op='start', data=data)
        except MaasApiHttpConflict as e:
            raise MaasApiNodeNotAcquired(e.status, e.message)
        cleave(s.__class__.__name__)
        return retval

    def stop(s, mode=None):
        response = s.__maas.post(u'/nodes/%s/' % s['system_id'], op='stop')
        raise MaasApiNotImplemented()

    @property
    def volume_groups(s):
        return VolumeGroups(s, s['system_id'])

    @volume_groups.setter
    def volue_groups(s, vgroups):
        pass
