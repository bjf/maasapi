
import unittest
from maasapi.client                     import MapiClient
from maasapi_test_case                  import MAASApiTestCase
import json
from maasapi.nodes                      import Nodes

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

        result = nodes.deployment_status([nodes[0]['system_id'], nodes[1]['system_id']])
        s.assertIs(type(result), dict)
        s.assertEqual(len(result), 2, msg='Expected 2 nodes but found %d instead.' % len(nodes))
        s.assertTrue(nodes[0]['system_id'] in result)
        s.assertTrue(nodes[1]['system_id'] in result)
        s.assertTrue(result[nodes[0]['system_id']] in ['Deployed', 'Not in deployment'])
        s.assertTrue(result[nodes[1]['system_id']] in ['Deployed', 'Not in deployment'])

        nodes[0].acquire()
        nodes[1].acquire()
        allocated = nodes.list_allocated()
        s.assertIs(type(allocated), Nodes)
        s.assertEqual(len(allocated), 2, msg='Expected 2 nodes but found %d instead.' % len(nodes))

        nodes[0].release()
        nodes[1].release()

        params = nodes.power_parameters()
        s.assertTrue(len(params) > 0)

        result = nodes.accept([nodes[0]['system_id'], nodes[1]['system_id']])

        nodes[0].release()
        nodes[1].release()

        result = nodes.accept_all()

        nodes[0].release()
        nodes[1].release()

        result = nodes.check_commissioning()
        print(json.dumps(result, sort_keys=True, indent=4))

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(NodesTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
