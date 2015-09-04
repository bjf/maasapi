
import unittest
from maasapi.client                     import MapiClient
from maasapi_test_case                  import MAASApiTestCase

class SSLKeysTestCase(MAASApiTestCase):

    def test_01(s):
        keys = MapiClient(s.url, s.creds).ssl_keys
        s.assertEqual(len(keys), 0)

        key =u'-----BEGIN CERTIFICATE-----\r\nMIID/zCCAuegAwIBAgIJANK8J6AYFS5MMA0GCSqGSIb3DQEBCwUAMIGVMQswCQYD\r\nVQQGEwJVUzEPMA0GA1UECAwGT3JlZ29uMREwDwYDVQQHDAhQb3J0bGFuZDEhMB8G\r\nA1UECgwYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMRAwDgYDVQQLDAdmb28ub3Jn\r\nMRAwDgYDVQQDDAdmb28ub3JnMRswGQYJKoZIhvcNAQkBFgxub25lQGZvby5jb20w\r\nHhcNMTUwOTA0MTM0MjI4WhcNMTYwOTAzMTM0MjI4WjCBlTELMAkGA1UEBhMCVVMx\r\nDzANBgNVBAgMBk9yZWdvbjERMA8GA1UEBwwIUG9ydGxhbmQxITAfBgNVBAoMGElu\r\ndGVybmV0IFdpZGdpdHMgUHR5IEx0ZDEQMA4GA1UECwwHZm9vLm9yZzEQMA4GA1UE\r\nAwwHZm9vLm9yZzEbMBkGCSqGSIb3DQEJARYMbm9uZUBmb28uY29tMIIBIjANBgkq\r\nhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuMSV3ftRS99XBUjDdaKq7sSYrcGpg/yq\r\nWdQelJJ5Htn9CJNE8aKrZQwniVtLXB4Q5Bx0xm6ffIQkO3K8gMZcgkEBJFJILD/i\r\nGchkXvQE8m4gMkwllimC14DYEcrRA12hpNpUutnKUx/6KGQaptd/zRPcDRatO9SK\r\n33uX25AnpnEqH7oky4VoaubHQdNlvAgXLJcXEWGgGga/SVRPkL8cVoXMdZkN9n7L\r\niZW9E5rfCISfAE6jIpLYzWQmXuYChI312pq4JMG7iOQL+1WjfssN6t6xMjGlw1V5\r\nI54NiqHjWkt4ZBrGW8Ve781AphLWOlzP55lMxgvbU8u5fXWvYTxLiQIDAQABo1Aw\r\nTjAdBgNVHQ4EFgQU1K7Ak+Qdew5bDguVj7AUvsGUfEkwHwYDVR0jBBgwFoAU1K7A\r\nk+Qdew5bDguVj7AUvsGUfEkwDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOC\r\nAQEAZfXb0mHrOChfP84EFn3fS77ADuMu5UFe4rvkhOshQD4thhsqXweOwu9g7AM8\r\nyuEYKvBiBI8HsUxGU++yTf0Nj2nHaRhyPu3tx3h4I0m187dItSut8rj80fzVXAKE\r\n8wK8AWkT5rRToDoMjA51yPD165EYYvCKBbN7AJYAYSKSOGn3r72G+8F1MyN3KgsO\r\nB+gIaXTOAouMe3PXHarF1J3Te9z2McV+THukRgm28RolbiqTTESxxz7GUxx+sfps\r\nzy4omSW+lPIBZ3xwHKmWRx9YfWj4B1tAqPZrrUqEjr5mc6gEcwGtVCaFSGQRBf6X\r\n2V86zNlxIyXLlCvisS0wVS2iSA==\r\n-----END CERTIFICATE-----\r\n'
        keys.new(key)
        s.assertEqual(len(keys), 1)
        s.assertEqual(keys[0]['key'], key)

        del(keys[0])
        s.assertEqual(len(keys), 0)

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TagsTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
