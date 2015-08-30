
from log                                import center, cleave

# User
#
class User(object):
    '''
    '''

    # __init__
    #
    def __init__(s, username=None, password=None, email=None, superuser=False):
        center(s.__class__.__name__)
        s.__username = username
        s.__email   = email
        s.__password = password
        s.__superuser = superuser

        cleave(s.__class__.__name__)

    @property
    def username(s):
        return s.__username

    @property
    def superuser(s):
        return s.__superuser

    @property
    def email(s):
        return s.__email

    @property
    def password(s):
        return s.__password

    def load_dict(s, d):
        s.__username  = d.get('username', None)
        s.__email     = d.get('email', None)
        s.__password  = d.get('password', None)
        s.__superuser = d.get('is_superuser', False)
        return s

    def to_rest_data(s):
        retval = []
        retval.append(('username', s.username))
        retval.append(('password', s.password))
        retval.append(('email', s.email))
        retval.append(('is_superuser', '1' if s.superuser else '0'))
        return retval
