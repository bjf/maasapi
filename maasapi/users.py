
from log                                import center, cleave, cdebug
from error                              import MapiError
from user                               import User

# Users
#
class Users(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__users = None
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
        retval = User().load_dict(s.__users[index])
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for item in s.__users:
            n = User().load_dict(item)
            yield n
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__users is None:
            response = s.__maas.get(u'/users/')
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__users = response.data
            cdebug('    fetched')
        cleave(s.__class__.__name__)

    # add
    #
    def add(s, user):
        center(s.__class__.__name__)
        if type(user) != User:
            raise TypeError, "Object is of type %s but must be of type User." % type(user)

        response = s.__maas.post(u'/users/', data=user.to_rest_data())
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        s.__users = None
        cleave(s.__class__.__name__)
        return response.data

