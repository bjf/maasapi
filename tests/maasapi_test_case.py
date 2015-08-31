import yaml
import unittest

class MAASApiTestCase(unittest.TestCase):

    def setUp(s):
        cfg = yaml.safe_load(file('maasapi-test.yaml'))
        s.url   = 'http://%s/MAAS/api/1.0' % cfg['maas']['ip']
        s.creds = cfg['maas']['creds']
        pass

