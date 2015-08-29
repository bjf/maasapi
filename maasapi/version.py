
from log                                import center, cleave

# Version
#
class Version(object):
    '''
    '''

    # __init__
    #
    def __init__(s, obj):
        center(s.__class__.__name__)
        if type(obj) != dict:
            raise TypeError, "Object is of type %s but must be of type dict." % type(obj)

        for k in obj:
            setattr(s, k, obj[k])

        cleave(s.__class__.__name__)

