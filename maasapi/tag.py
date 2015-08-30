
from log                                import center, cleave

# Tag
#
class Tag(object):
    '''
    '''

    # __init__
    #
    def __init__(s, name=None, comment=None, definition=None):
        center(s.__class__.__name__)
        s.__name       = name
        s.__comment    = comment
        s.__definition = definition
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
        retval.append(('name', s.name))
        retval.append(('comment', s.comment))
        retval.append(('ddefinition', s.definition))
        cleave(s.__class__.__name__)
        return retval
