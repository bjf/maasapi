#!/usr/bin/env python
#
# Copyright 2012-2015 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

# The code in this file was derived from the api.py file in maascli.
#

from __future__                         import print_function

import sys
import re
import httplib2
from textwrap                           import dedent, wrap
from functools                          import partial
from apiclient.multipart                import build_multipart_message, encode_multipart_message
from urlparse                           import urlparse
from apiclient.utils                    import urlencode
from email.message                      import Message
from apiclient                          import maas_client as maas
import json

from log                                import center, cleave, cdebug, Clog
from response                           import Response
from error                              import MaasApiUnknownError, MaasApiCertificateVerificationError, MaasApiHttpServiceUnavailable

#--------------------------------------------------------------------------------


def http_request(url, method, body=None, headers=None,
                 insecure=False):
    """Issue an http request."""
    center('api.http_request')
    cdebug('         url: %s' % url)
    cdebug('      method: %s' % method)
    cdebug('        body: %s' % body)
    cdebug('     headers: %s' % headers)
    cdebug('    insecure: %s' % insecure)
    http = httplib2.Http(disable_ssl_certificate_validation=insecure)
    try:
        cleave('api.http_request')
        return http.request(url, method, body=body, headers=headers)
    except httplib2.SSLHandshakeError:
        cleave('api.http_request')
        raise MaasApiCertificateVerificationError(0,
            "Certificate verification failed, use --insecure/-k to "
            "disable the certificate check.")

def is_response_textual(response):
    """Is the response body text?"""
    center('api.is_response_textual')
    content_type = get_response_content_type(response)
    cdebug('content_type: %s' % content_type)
    retval = (content_type.endswith("/json") or content_type.startswith("text/"))
    cleave('api.is_response_textual (%s)' % retval)
    return retval



def print_headers(headers, file=sys.stdout):
    """Show an HTTP response in a human-friendly way.

    :type headers: :class:`httplib2.Response`, or :class:`dict`
    """
    # Function to change headers like "transfer-encoding" into
    # "Transfer-Encoding".
    cap = lambda header: "-".join(
        part.capitalize() for part in header.split("-"))
    # Format string to prettify reporting of response headers.
    form = "%%%ds: %%s" % (
        max(len(header) for header in headers) + 2)
    # Print the response.
    for header in sorted(headers):
        print(form % (cap(header), headers[header]), file=file)

def get_response_content_type(response):
    """Returns the response's content-type, without parameters.

    If the content-type was not set in the response, returns `None`.

    :type response: :class:`httplib2.Response`
    """
    center('api.get_response_content_type')
    try:
        content_type = response["content-type"]
    except KeyError:
        cleave('api.get_response_content_type')
        return None
    else:
        # It seems odd to create a Message instance here, but at the time of
        # writing it's the only place that has the smarts to correctly deal
        # with a Content-Type that contains a charset (or other parameters).
        message = Message()
        message.set_type(content_type)
        cleave('api.get_response_content_type')
        return message.get_content_type()

# RestClient
#
class RestClient(object):
    '''
    '''

    def __init__(s, url, creds):
        center(s.__class__.__name__)
        cdebug('      url: %s' % url)
        cdebug('    creds: %s' % creds)
        s.root  = url
        s.creds = creds
        cleave(s.__class__.__name__)

    """
    A generic MAAS API action.

    This is used as a base for creating more specific commands; see
    `register_actions`.

    **Note** that this class conflates two things: CLI exposure and API
    client. The client in apiclient.maas_client is not quite suitable yet, but
    it should be iterated upon to make it suitable.
    """

    # Override these in subclasses; see `register_actions`.
    #profile = handler = action = None

    #uri = property(lambda self: self.handler["uri"])
    #method = property(lambda self: self.action["method"])
    #credentials = property(lambda self: self.profile["credentials"])
    #op = property(lambda self: self.action["op"])

    @classmethod
    def call(cls, uri, op, method, creds, data=[]):
        center('RestClient.call')
        # TODO: this is el-cheapo URI Template
        # <http://tools.ietf.org/html/rfc6570> support; use uritemplate-py
        # <https://github.com/uri-templates/uritemplate-py> here?
        #uri = self.uri.format(**vars(options))

        # Bundle things up ready to throw over the wire.
        uri, body, headers = cls.prepare_payload(op, method, uri, data)

        # Headers are returned as a list, but they must be a dict for
        # the signing machinery.
        headers = dict(headers)

        # Sign request if credentials have been provided.
        credentials = creds.split(':')
        if credentials is not None:
            cls.sign(uri, headers, credentials)

        # Use httplib2 instead of urllib2 (or MAASDispatcher, which is based
        # on urllib2) so that we get full control over HTTP method. TODO:
        # create custom MAASDispatcher to use httplib2 so that MAASClient can
        # be used.
        response, content = http_request(uri, method, body=body, headers=headers, insecure=False)

        # Compare API hashes to see if our version of the API is old.
        #self.compare_api_hashes(self.profile, response)

        # Output.
        #cdebug('response.status: %d' % response.status)
        #cls.print_debug(response)
        #cls.print_response(response, content)

        # 2xx status codes are all okay.
        if response.status // 100 != 2:
            cleave('MaiClient.call')
            if response.status == 503:
                raise MaasApiHttpServiceUnavailable(response.status, content)
            else:
                raise MaasApiUnknownError(response.status, content)

        if is_response_textual(response):
            try:
                retval = Response(True, json.loads(content))
                if Clog.dbg:
                    cdebug('content: %s' % content)
            except ValueError:
                # The content is not a json string. Just assume it's a plain string.
                #
                retval = Response(True, content)
        else:
            retval = Response(True, content)
        cleave('RestClient.call')
        return retval

    @staticmethod
    def compare_api_hashes(profile, response):
        """Compare the local and remote API hashes.

        If they differ -- or the remote side reports a hash and there is no
        hash stored locally -- then show a warning to the user.
        """
        center('RestClient.compare_api_hashes')
        hash_from_response = response.get("X-MAAS-API-Hash".lower())
        if hash_from_response is not None:
            hash_from_profile = profile["description"].get("hash")
            if hash_from_profile != hash_from_response:
                warning = dedent("""\
                WARNING! The API on the server differs from the description
                that is cached locally. This may result in failed API calls.
                Refresh the local API description with `maas refresh`.
                """)
                warning_lines = wrap(warning, width=70, initial_indent="*** ", subsequent_indent="*** ")
                print("**********" * 7, file=sys.stderr)
                for warning_line in warning_lines:
                    print(warning_line, file=sys.stderr)
                print("**********" * 7, file=sys.stderr)
        cleave('RestClient.compare_api_hashes')

    @staticmethod
    def name_value_pair(string):
        """Ensure that `string` is a valid ``name:value`` pair.

        When `string` is of the form ``name=value``, this returns a
        2-tuple of ``name, value``.

        However, when `string` is of the form ``name@=value``, this
        returns a ``name, opener`` tuple, where ``opener`` is a function
        that will return an open file handle when called. The file will
        be opened in binary mode for reading only.
        """
        center('RestClient.name_value_pair')
        parts = re.split(r'(=|@=)', string, 1)
        if len(parts) == 3:
            name, what, value = parts
            if what == "=":
                cleave('RestClient.name_value_pair (%s : %s)' % (name, value))
                return name, value
            elif what == "@=":
                cleave('RestClient.name_value_pair')
                return name, partial(open, value, "rb")
            else:
                cleave('RestClient.name_value_pair')
                raise AssertionError(
                    "Unrecognised separator %r" % what)
        else:
            cleave('RestClient.name_value_pair')
            raise CommandError(
                "%r is not a name=value or name@=filename pair" % string)

    @classmethod
    def prepare_payload(cls, op, method, uri, data):
        """Return the URI (modified perhaps) and body and headers.

        - For GET requests, encode parameters in the query string.

        - Otherwise always encode parameters in the request body.

        - Except op; this can always go in the query string.

        :param method: The HTTP method.
        :param uri: The URI of the action.
        :param data: An iterable of ``name, value`` or ``name, opener``
            tuples (see `name_value_pair`) to pack into the body or
            query, depending on the type of request.
        """
        center('RestClient.prepare_payload')
        cdebug('    op : %s' % op)
        cdebug('method : %s' % method)
        cdebug('   uri : %s' % uri)
        cdebug('  data : %s' % data)
        query = [] if op is None else [("op", op)]

        def slurp(opener):
            with opener() as fd:
                return fd.read()

        if method == "GET":
            query.extend(
                (name, slurp(value) if callable(value) else value)
                for name, value in data)
            body, headers = None, []
        else:
            if data is None or len(data) == 0:
                body, headers = None, []
            else:
                cdebug('encode multipart')
                message = build_multipart_message(data)
                headers, body = encode_multipart_message(message)

        uri = urlparse(uri)._replace(query=urlencode(query)).geturl()
        cleave('RestClient.prepare_payload')
        cdebug('    uri : %s' % uri)
        cdebug('   body : %s' % body)
        cdebug('headers : %s' % headers)
        return uri, body, headers

    @staticmethod
    def sign(uri, headers, credentials):
        """Sign the URI and headers."""
        center('RestClient.sign')
        auth = maas.MAASOAuth(*credentials)
        auth.sign_request(uri, headers)
        cleave('RestClient.sign')

    @staticmethod
    def print_debug(response):
        """Dump the response line and headers to stderr."""
        print(response.status, response.reason, file=sys.stderr)
        print(file=sys.stderr)
        print_headers(response, file=sys.stderr)
        print(file=sys.stderr)

    @classmethod
    def print_response(cls, response, content, file=sys.stdout):
        """Write the response's content to stdout.

        If the response is textual, a trailing \n is appended.
        """
        if file.isatty():
            if response.status // 100 == 2:
                file.write("Success.\n")
                if is_response_textual(response) and response.status // 100 == 2:
                    file.write("Machine-readable output follows:\n")
                print(content)

            file.write(content)

            if is_response_textual(response):
                file.write("\n")
        else:
            file.write(content)

