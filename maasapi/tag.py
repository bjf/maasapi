
from log                                import center, cleave
from nodes                              import Nodes
from error                              import MapiError

# Tag
#
class Tag(object):
    '''
    '''

    # __init__
    #
    def __init__(s, client=None, name=None, comment=None, definition=None):
        center(s.__class__.__name__)
        s.__name       = name
        s.__comment    = comment
        s.__definition = definition
        s.__maas       = client
        cleave(s.__class__.__name__)

    @property
    def name(s):
        return s.__name

    @property
    def comment(s):
        return s.__comment

    @property
    def definition(s):
        return s.__definition

    @property
    def nodes(s):
        return Nodes(s.__maas, uri=u'/tags/%s/' % s.name, op='nodes')

    def rebuild(s):
        center(s.__class__.__name__)
        response = s.__maas.post(u'/tags/%s/' % s.name, op='rebuild')
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        cleave(s.__class__.__name__)
        return response.data

    def update(s, name=None, comment=None, definition=None):
        center(s.__class__.__name__)
        utag = Tag(client=s.__maas, name=name, comment=comment, definition=definition)
        utag_data = utag.to_rest_data()

        response = s.__maas.put(u'/tags/%s/' % s.name, data=utag_data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)

        cleave(s.__class__.__name__)
        return response.data

    def add_nodes(s, system_ids=[], description=None, nodegroup=None):
        center(s.__class__.__name__)
        utag_data = []
        utag_data.append(('add', ','.join(system_ids)))
        if description:
            utag_data.append(('description', description))
        if nodegroup:
            utag_data.append(('nodegroup', nodegroup))
        response = s.__maas.post(u'/tags/%s/' % s.name, op='update_nodes', data=utag_data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)

        cleave(s.__class__.__name__)
        return response.data

    def remove_nodes(s, system_ids=[], description=None, nodegroup=None):
        center(s.__class__.__name__)
        utag_data = []
        utag_data.append(('remove', ','.join(system_ids)))
        if description:
            utag_data.append(('description', description))
        if nodegroup:
            utag_data.append(('nodegroup', nodegroup))
        response = s.__maas.post(u'/tags/%s/' % s.name, op='update_nodes', data=utag_data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)

        cleave(s.__class__.__name__)
        return response.data

    def load_dict(s, d):
        center(s.__class__.__name__)
        s.__name       = d.get('name', None)
        s.__comment    = d.get('comment', None)
        s.__definition = d.get('definition', None)
        cleave(s.__class__.__name__)
        return s

    def to_rest_data(s):
        center(s.__class__.__name__)
        retval = []
        if s.name:
            retval.append(('name', s.name))
        if s.comment:
            retval.append(('comment', s.comment))
        if s.definition:
            retval.append(('definition', s.definition))
        cleave(s.__class__.__name__)
        return retval
