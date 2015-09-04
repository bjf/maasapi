#!/usr/bin/env python
#

from log                                import center, cleave, cdebug
from error                              import MapiError
from node                               import Node

# Nodes
#
class Nodes(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, op='list', uri=u'/nodes/'):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__resources = None
        s.__op = op
        s.__uri = uri
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
        retval = Node(s.__maas, s.__resources[index])
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for group in s.__resources:
            n = Node(s.__maas, group)
            yield n
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__resources is None:
            response = s.__maas.get(s.__uri, op=s.__op)
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__resources = response.data
            cdebug('    fetched')
        cleave(s.__class__.__name__)

    # deployment_status()
    #
    def deployment_status(s, node_ids):
        center(s.__class__.__name__)
        data = []
        for n in node_ids:
            data.append(('nodes', n))
        response = s.__maas.get(u'/nodes/', op='deployment_status', data=data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        cleave(s.__class__.__name__)
        return response.data

    # list_allocated()
    #
    def list_allocated(s):
        center(s.__class__.__name__)
        retval = Nodes(s.__maas, op='list_allocated')
        cleave(s.__class__.__name__)
        return retval

    # power_parameters()
    #
    def power_parameters(s, node_ids=[]):
        center(s.__class__.__name__)
        data = []
        for n in node_ids:
            data.append(('nodes', n))
        response = s.__maas.get(u'/nodes/', op='power_parameters', data=data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        cleave(s.__class__.__name__)
        return response.data

    # accept()
    #
    def accept(s, node_ids=[]):
        center(s.__class__.__name__)
        data = []
        for n in node_ids:
            data.append(('nodes', n))
        response = s.__maas.post(u'/nodes/', op='accept', data=data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        cleave(s.__class__.__name__)
        return response.data

    # accept_all()
    #
    def accept_all(s):
        center(s.__class__.__name__)
        response = s.__maas.post(u'/nodes/', op='accept')
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        cleave(s.__class__.__name__)
        return response.data

    # acquire()
    #
    def acquire(s, name=None, arch=None,
                   cpu_count=None, mem=None,
                   tags=[], not_tags=[],
                   networks=[], not_networks=[],
                   connected_to=[], not_connected_to=[],
                   zone=None, not_in_zone=[], agent_name=None):
        center(s.__class__.__name__)
        data = []
        if name:
            data.append(('name', name))
        if arch:
            data.append(('arch', arch))
        if cpu_count:
            data.append(('cpu_count', cpu_count))
        if mem:
            data.append(('mem', mem))
        for t in tags:
            data.append(('tags', t))
        for t in not_tags:
            data.append(('not_tags', t))
        for n in networks:
            data.append(('networks', n))
        for n in not_networks:
            data.append(('not_networks', n))
        for c in connected_to:
            data.append(('connected_to', c))
        for c in not_connected_to:
            data.append(('not_connected_to', c))
        for z in zone:
            data.append(('zone', z))
        for z in not_in_zone:
            data.append(('not_in_zone', z))
        if agent_name:
            data.append(('agent_name', agent_name))


        response = s.__maas.post(u'/nodes/', op='accept', data=data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        cleave(s.__class__.__name__)
        return response.data

    # check_commissioning()
    #
    def check_commissioning(s):
        center(s.__class__.__name__)
        response = s.__maas.post(u'/nodes/', op='check_commissioning')
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        cleave(s.__class__.__name__)
        return response.data

    # new()
    #
    def new(s, architecture,
               mac_addresses,
               autodetect_nodegroup=True,
               min_hwe_kernel=None,
               subarchitecture=None,
               hostname=None,
               power_type=None,
               nodegroup=None):
        center(s.__class__.__name__)
        data = []
        data.append(('architecture', architecture))
        data.append(('mac_addresses', mac_addresses))
        data.append(('autodetect_nodegroup', autodetect_nodegroup))
        if min_hwe_kernel:
            data.append(('min_hwe_kenrel', min_hwe_kernel))
        if subarchitecture:
            data.append(('subarchitecture', subarchitecture))
        if hostname:
            data.append(('hostname', hostname))
        if power_type:
            data.append(('power_type', power_type))
        if nodegroup:
            data.append(('nodegroup', nodegroup))

        response = s.__maas.post(u'/nodes/', op='new', data=data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        cleave(s.__class__.__name__)
        return response.data

    # release()
    #
    def release(s, node_ids=[]):
        center(s.__class__.__name__)
        data = []
        for n in node_ids:
            data.append(('nodes', n))
        response = s.__maas.post(u'/nodes/', op='release', data=data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        cleave(s.__class__.__name__)
        return response.data

    # set_zone()
    #
    def set_zone(s, zone=None, node_ids=[]):
        center(s.__class__.__name__)
        data = []
        if zone:
            data.append(('zone', zone))
        for n in node_ids:
            data.append(('nodes', n))
        response = s.__maas.post(u'/nodes/', op='set_zone', data=data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        cleave(s.__class__.__name__)
        return response.data
