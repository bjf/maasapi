
import unittest
from maasapi.client                     import MapiClient
from maasapi_test_case                  import MAASApiTestCase
from maasapi.error                      import MaasApiNodeStateReady
import json

class NodeTestCase(MAASApiTestCase):

    def tearDown(s):
        pass

    def test_01(s):
        nodes = MapiClient(s.url, s.creds).nodes

        s.assertEqual(len(nodes), 4, msg='Expected 4 nodes but found %d instead.' % len(nodes))

        node = nodes[0]
        s.assertIsNotNone(node)
        print(json.dumps(node, sort_keys=True, indent=4))

        for node in nodes:
            if node['hostname'] == 'nuc1.maas':
                break

        # node.power_state
        #
        pstate = node.power_state
        s.assertEqual(pstate, 'on')
        print(pstate)

        # node.details
        #
        details = node.details
        s.assertIsNotNone(details)
        #print(json.dumps(details, sort_keys=True, indent=4))
        #print(details)

        # node.power_parameters
        #
        params = node.power_parameters
        s.assertIsNotNone(params)
        s.assertEqual(params['power_address'], '10.10.10.100')
        s.assertEqual(params['power_pass'], '1Pa**word')
        s.assertEqual(params['mac_address'], 'ec:a8:6b:fa:91:64')

        # node.abort()
        #
        try:
            result = node.abort()
            s.assertTrue(False, 'The node.abort() should have thrown an exception.')
        except MaasApiNodeStateReady as e:
            s.assertTrue(True)

        # node.commission()
        #
        result = node.commission()
        print(json.dumps(node, sort_keys=True, indent=4))

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TagsTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
