
import unittest
from maasapi.client                     import MapiClient
from maasapi_test_case                  import MAASApiTestCase
import json

class NodesTestCase(MAASApiTestCase):

    def tearDown(s):
        pass

    def test_01(s):
        nodes = MapiClient(s.url, s.creds).nodes

        s.assertEqual(len(nodes), 4, msg='Expected 4 nodes but found %d instead.' % len(nodes))

        node = nodes[0]
        s.assertIsNotNone(node)

        for node in nodes:
            s.assertIsNotNone(node)
            print(json.dumps(node, sort_keys=True, indent=4))


if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TagsTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
