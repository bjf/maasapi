
import unittest
from maasapi.client                     import MapiClient
from maasapi_test_case                  import MAASApiTestCase
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

        pstate = node.power_state
        s.assertEqual(pstate, 'on')
        print(pstate)

        details = node.details
        s.assertIsNotNone(details)
        #print(json.dumps(details, sort_keys=True, indent=4))
        #print(details)

        params = node.power_parameters
        s.assertIsNotNone(params)
        s.assertEqual(params['power_address'], '10.10.10.100')
        s.assertEqual(params['power_pass'], '1Pa**word')
        s.assertEqual(params['mac_address'], 'ec:a8:6b:fa:91:64')

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TagsTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
