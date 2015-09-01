
import unittest
from maasapi.client                     import MapiClient
from maasapi_test_case                  import MAASApiTestCase

class UsersTestCase(MAASApiTestCase):

    def setUp(s):
        MAASApiTestCase.setUp(s)
        s.defined = {
            'jenkins' : {             'admin' : True,  'email' : 'jenkins@nowhere.org' },
            'maas' : {                'admin' : True,  'email' : 'brad.figg@canonical.com' },
            'maas-init-node' : {      'admin' : False, 'email' : '' },
            'maas-nodegroup-worker' : { 'admin' : False, 'email' : 'maas-nodegroup-worker@localhost' },
        }

    def tearDown(s):
        pass

    def test_users(s):
        users = MapiClient(s.url, s.creds).users

        # There are 4 users defined on the maas server that I'm using for testing.
        #
        s.assertEqual(len(users), 4)

        #username, email, password, is_superuser
        print(len(users))

        for user in users:
            s.assertIsNotNone(s.defined[user.username])
            s.assertEqual(user.superuser, s.defined[user.username]['admin'])
            s.assertEqual(user.email, s.defined[user.username]['email'])

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TagsTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
