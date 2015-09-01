
import unittest
from maasapi.client                     import MapiClient
from maasapi_test_case                  import MAASApiTestCase

class ZonesTestCase(MAASApiTestCase):

    def tearDown(s):
        # Cleanup (delete) any zones that were created during testing. The only
        # zone that is not created by testing is the 'default' zone.
        #
        zones = MapiClient(s.url, s.creds).zones
        for z in zones:
            if z.name == 'default':
                continue
            del(zones[z.name])

    def test_zones(s):
        zones = MapiClient(s.url, s.creds).zones


        # Should only be the default zone.
        #
        s.assertEqual(len(zones), 1)

        # Add one
        #
        zones['foo'] = 'bar'
        s.assertEqual(len(zones), 2)

        # Delete the one we just added
        #
        del(zones['foo'])
        s.assertEqual(len(zones), 1)

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TagsTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
