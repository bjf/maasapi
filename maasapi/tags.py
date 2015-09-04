
from log                                import center, cleave, cdebug
from error                              import MapiError
from tag                                import Tag

# Tags
#
class Tags(object):
    '''
    '''

    # __init__
    #
    def __init__(s, maas):
        center(s.__class__.__name__)
        s.__maas = maas
        s.__tags = None
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
        retval = Tag(client=s.__maas).load_dict(s.__tags[index])
        cleave(s.__class__.__name__)
        return retval

    # __iter__
    #
    def __iter__(s):
        center(s.__class__.__name__)
        s.__fetch_if_needed()
        for item in s.__tags:
            n = Tag(client=s.__maas).load_dict(item)
            yield n
        cleave(s.__class__.__name__)

    # __fetch_if_needed
    #
    def __fetch_if_needed(s):
        center(s.__class__.__name__)
        if s.__tags is None:
            response = s.__maas.get(u'/tags/', op='list')
            if not response.ok:
                if type(response.data) == str:
                    cleave(s.__class__.__name__)
                    raise MapiError(response.data)

            s.__tags = response.data
            cdebug('    fetched')
        cleave(s.__class__.__name__)

    # new
    #
    def new(s, name, comment=None, definition=None, kernel_opts=None):
        center(s.__class__.__name__)
        data = []
        data.append(('name', name))
        if comment:
            data.append(('comment', comment))
        if definition:
            data.append(('definition', definition))
        if kernel_opts:
            data.append(('kernel_opts', kernel_opts))

        response = s.__maas.post(u'/tags/', op='new', data=data)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        s.__tags = None
        cleave(s.__class__.__name__)
        return response.data

    # delete
    #
    def delete(s, tag):
        center(s.__class__.__name__)
        if type(tag) != Tag:
            raise TypeError, "Object is of type %s but must be of type Tag." % type(tag)

        response = s.__maas.delete(u'/tags/%s/' % tag.name)
        if not response.ok:
            if type(response.data) == str:
                cleave(s.__class__.__name__)
                raise MapiError(response.data)
        s.__tags = None
        cleave(s.__class__.__name__)
        return response.data

