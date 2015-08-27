#!/usr/bin/env python
#

# MapiError
#
class MapiError(Exception):
    '''
    '''
    # __init__
    #
    def __init__(s, reason):
        s.reason = reason

# MaasApiUnknownError
#
class MaasApiUnknownError(Exception):
    '''
    Place holder exception until we determine a more specific exception to
    throw.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        s.status  = status
        s.message = msg

# MaasApiCertificateVerificationError
#
class MaasApiCertificateVerificationError(Exception):
    '''
    The MAAS credentials that are specified are not valid for this MAAS server.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        s.status  = status
        s.message = msg

# MaasApiPowerResponseTimeout
#
class MaasApiPowerResponseTimeout(Exception):
    '''
    While attempting to get the power state for a node the response back was
    an HTTP 503 with 'Timed out waiting for power response'. It's possible
    the node is 'broken'.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        s.status  = status
        s.message = msg

# MaasApiHttpServiceUnavailable
#
class MaasApiHttpServiceUnavailable(Exception):
    '''
    While communicating with the MAAS rest interface we got back an HTTP 503.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        s.status  = status
        s.message = msg

