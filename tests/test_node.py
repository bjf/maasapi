
import unittest
from maasapi.client                     import MapiClient
from maasapi.error                      import (
                                                    MaasApiUnknownError,
                                                    MaasApiNodeBadMACAddress,
                                                    MaasApiNodeStateReady,
                                               )
from maasapi.node                       import Node
from maasapi_test_case                  import MAASApiTestCase
import json
from time                               import sleep

class NodeTestCase(MAASApiTestCase):

    def tearDown(s):
        pass

    def test_01(s):
        try:
            nodes = MapiClient(s.url, s.creds).nodes

            s.assertEqual(len(nodes), 4, msg='Expected 4 nodes but found %d instead.' % len(nodes))

            node = nodes[0]
            s.assertIsNotNone(node)

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
            s.assertTrue(type(result), Node)
            #print(json.dumps(node, sort_keys=True, indent=4))

            # node.mark_broken()
            #
            result = node.mark_broken(description='MAAS Api Testing')
            s.assertTrue(type(result), Node)
            #print(json.dumps(result, sort_keys=True, indent=4))

            sleep(1)

            # node.mark_fixed()
            #
            result = node.mark_fixed()
            s.assertTrue(type(result), Node)
            #print(json.dumps(result, sort_keys=True, indent=4))

            # node.release()
            #
            #print(json.dumps(node, sort_keys=True, indent=4))
            result = node.release()
            s.assertTrue(type(result), Node)
            #print(json.dumps(result, sort_keys=True, indent=4))

            # node.claim_sticky_ip_address()
            #
            try:
                result = node.claim_sticky_ip_address(mac_address='12:34:56:78:ab:cd', requested_address='10.10.11.111')
                s.assertTrue(False, 'Should have raise a MaasApiNodeBadMACAddress exception.')
            except MaasApiNodeBadMACAddress as e:
                s.assertTrue(True)

            #  sleep(2)

            #  result = node.claim_sticky_ip_address(requested_address='10.10.11.111')
            #  print(json.dumps(result, sort_keys=True, indent=4))

            #  sleep(2)

            #  # node.release_sticky_ip_address()
            #  #
            #  result = node.release_sticky_ip_address()
            #  print(json.dumps(result, sort_keys=True, indent=4))

        except MaasApiUnknownError as e:
            print(e.status)
            print(e.message)
            raise e

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TagsTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
