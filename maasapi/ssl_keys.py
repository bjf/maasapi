
from log                                import center, cleave, cdebug
from error                              import MapiError, MaasApiHttpBadRequest, MaasApiBadSSLKey

# SSLKeys
#
class SSLKeys(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__keys = None
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
        retval = s.__keys[index]
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for item in s.__keys:
            yield item
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__keys is None:
            response = s.__maas.get(u'/account/prefs/sslkeys/', op='list')
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__keys = response.data
            cdebug('    fetched')
        cleave(s.__class__.__name__)

    # new
    #
    def new(s, key):
        center(s.__class__.__name__)
        data = []
        data.append((u'key', unicode(key)))
        try:
            response = s.__maas.post(u'/account/prefs/sslkeys/', op='new', data=data)
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)
            s.__keys = None
        except MaasApiHttpBadRequest as e:
            raise MaasApiBadSSLKey(e.status, e.message)
        cleave(s.__class__.__name__)
        return response.data

    # __delitem__
    #
    def __delitem__(s, key):
        center(s.__class__.__name__)
        response = s.__maas.delete(u'/account/prefs/sslkeys/%s/' % s.__keys[key]['id'])
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        s.__keys = None
        cleave(s.__class__.__name__)

