#
# Copyright 2015, Canonical Ltd
#

import json
import logging
from urllib2                            import HTTPError

from apiclient                          import maas_client as maas
from mapi.response                      import Response

log = logging.getLogger('mapi')
OK = 200

class RestClient():
    """
    Talk to the remote MAAS via the restful api.
    """

    def __init__(self, api_url, api_key, *args, **kwargs):
        if api_url.find('/api/') < 0:
            api_url = api_url + '/api/1.0'
        self._client = None
        self._oauth = None
        self.api_key = api_key
        self.api_url = api_url

    @property
    def client(self):
        """
        MAAS client

        :rtype: MAASClient
        """
        if not self._client:
            self._client = maas.MAASClient(auth=self.oauth,
                                           dispatcher=maas.MAASDispatcher(),
                                           base_url=self.api_url)
        return self._client

    @property
    def oauth(self):
        """
        MAAS OAuth information for interacting with the MAAS API.

        :rtype: MAASOAuth
        """
        if not self._oauth:
            if self.api_key:
                api_key = self.api_key.split(':')
                self._oauth = maas.MAASOAuth(consumer_key=api_key[0],
                                             resource_token=api_key[1],
                                             resource_secret=api_key[2])
        return self._oauth

    def _get(self, path, **kwargs):
        """
        Issues a GET request to the MAAS REST API, returning the data
        from the query in the python form of the json data.
        """
        try:
            response = self.client.get(path, **kwargs)
            payload = response.read()
            log.debug("Request %s results: [%s] %s", path, response.getcode(),
                      payload)

            if response.getcode() == OK:
                return Response(True, json.loads(payload))
            else:
                return Response(False, payload)
        except Exception as e:
            log.error("Error encountered: %s for %s with params %s",
                      e.message, path, str(kwargs))
            return Response(False, None)

    def _post(self, path, op, **kwargs):
        """
        Issues a POST request to the MAAS REST API.
        """
        try:
            response = self.client.post(path, op, **kwargs)
            payload = response.read()
            log.debug("Request %s results: [%s] %s", path, response.getcode(),
                      payload)

            if response.getcode() == OK:
                return Response(True, json.loads(payload))
            else:
                return Response(False, payload)
        except HTTPError as e:
            log.error("Error encountered: %s for %s with params %s",
                      str(e), path, str(kwargs))
            return Response(False, None)
        except Exception as e:
            # import pdb
            # pdb.set_trace()
            log.error("Request raised exception: %s", e)
            return Response(False, None)

    def _put(self, path, **kwargs):
        """
        Issues a PUT request to the MAAS REST API.
        """
        try:
            response = self.client.put(path, **kwargs)
            payload = response.read()
            log.debug("Request %s results: [%s] %s", path, response.getcode(),
                      payload)
            if response.getcode() == OK:
                return Response(True, payload)
            else:
                return Response(False, payload)
        except HTTPError as e:
            log.error("Error encountered: %s with details: %s for %s with "
                      "params %s", e, e.read(), path, str(kwargs))
            return Response(False, None)
        except Exception as e:
            log.error("Request raised exception: %s", e)
            return Response(False, None)

    def _get_system_id(self, obj):
        """
        Returns the system_id from an object or the object itself
        if the system_id is not found.
        """
        if 'system_id' in obj:
            return obj.system_id
        return obj

    def _get_uuid(self, obj):
        """
        Returns the UUID for the MAAS object. If the object has the attribute
        'uuid', then this method will return obj.uuid, otherwise this method
        will return the object itself.
        """
        if hasattr(obj, 'uuid'):
            return obj.uuid
        return obj

