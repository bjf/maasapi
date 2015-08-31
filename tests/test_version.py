
import re
import unittest
from maasapi.client                     import MapiClient
from maasapi_test_case                  import MAASApiTestCase

class VersionTestCase(MAASApiTestCase):

    def test_version(s):
        version = MapiClient(s.url, s.creds).version.version

        m = re.match(r'\d+.\d+.\d+\+bzr\d+\-\d+ubuntu\d+', version)
        s.assertIsNotNone(m, msg='%s does not match the regular expression' % version)

    def test_subversion(s):
        subversion = MapiClient(s.url, s.creds).version.subversion
        s.assertEqual('trusty1', subversion)

    def test_capabilities(s):
        capabilities = MapiClient(s.url, s.creds).version.capabilities

        s.assertTrue(len(capabilities) >= 3, msg='capabilities: %s' % capabilities)

        caps = ['networks-management', 'static-ipaddresses', 'ipv6-deployment-ubuntu']
        for c in caps:
            s.assertIn(c, capabilities)

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(VersionTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
