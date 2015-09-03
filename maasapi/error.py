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

# MaasApiNotImplemented
#
class MaasApiNotImplemented(Exception):
    '''
    Place holder exception until we implement the method/property affected.
    '''
    # __init__
    #
    def __init__(s):
        s.status  = 0
        s.message = "This method/property has not been implemented."

# MaasApiStandardException
#
class MaasApiStandardException(Exception):
    '''
    Generic base, exception class.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        s.status  = status
        s.message = msg

# MaasApiUnknownError
#
class MaasApiUnknownError(MaasApiStandardException):
    '''
    Place holder exception until we determine a more specific exception to
    throw.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        super(MaasApiStandardException, s).__init__(status, msg)

# MaasApiCertificateVerificationError
#
class MaasApiCertificateVerificationError(MaasApiStandardException):
    '''
    The MAAS credentials that are specified are not valid for this MAAS server.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        super(MaasApiStandardException, s).__init__(status, msg)

# MaasApiPowerResponseTimeout
#
class MaasApiPowerResponseTimeout(MaasApiStandardException):
    '''
    While attempting to get the power state for a node the response back was
    an HTTP 503 with 'Timed out waiting for power response'. It's possible
    the node is 'broken'.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        super(MaasApiStandardException, s).__init__(status, msg)

# MaasApiNodeStateSteady
#
class MaasApiNodeStateSteady(MaasApiStandardException):
    '''
    A node abort failed. The node was in a Ready state, not performing any
    operation that could be aborted.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        super(MaasApiStandardException, s).__init__(status, msg)

# MaasApiHttpServiceUnavailable
#
class MaasApiHttpServiceUnavailable(MaasApiStandardException):
    '''
    While communicating with the MAAS rest interface we got back an HTTP 503.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        super(MaasApiStandardException, s).__init__(status, msg)

# MaasApiHttpConflict
#
class MaasApiHttpConflict(MaasApiStandardException):
    '''
    While communicating with the MAAS rest interface we got back an HTTP 409.
    '''
    # __init__
    #
    def __init__(s, status, msg):
        super(MaasApiStandardException, s).__init__(status, msg)

