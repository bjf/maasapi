#!/usr/bin/env python
#

from log                                import center, cleave, cdebug, Clog

# MyDict
#
class MyDict(dict):
    '''
    '''

    # __init__
    #
    def __init__(s, maas, obj):
        center(s.__class__.__name__)

        dict.__init__(s, obj)

        cleave(s.__class__.__name__)

    # dump
    #
    def dump(s, d=None, title=None, key=None, more=False):
        if d is None:
            d = dict(s)

        if title:
            cdebug(title)
            cdebug('-------------------------------------------------------------------------------------------')
        if type(d) == dict:
            if key is not None:
                cdebug('%s : {' % key)
            else:
                cdebug('{')
            for k in d:
                if type(d[k]) == dict or type(d[k]) == list:
                    Clog.indent += 4
                    s.dump(d[k], key=k, more=True)
                    Clog.indent -= 4
                else:
                    cdebug('    %s : %s,' % (k, d[k]))
            if more:
                cdebug('},')
            else:
                cdebug('}')
        elif type(d) == list:
            if key is not None:
                cdebug('%s : [' % key)
            else:
                cdebug('[')
            for k in d:

                if type(k) == dict :
                    Clog.indent += 4
                    s.dump(k, more=True)
                    Clog.indent -= 4
                elif type(k) == list:
                    Clog.indent += 4
                    s.dump(k, key=k, more=True)
                    Clog.indent -= 4
                else:
                    cdebug('    %s,' % (k))

            if more:
                cdebug('],')
            else:
                cdebug(']')
        else:
            cdebug('    %s,' % (d))
