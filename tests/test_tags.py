
import re
import unittest
from maasapi.client                     import MapiClient
from maasapi.tag                        import Tag
from maasapi_test_case                  import MAASApiTestCase

class TagsTestCase(MAASApiTestCase):

    def tearDown(s):
        # Cleanup (delete) any tags that were created during testing.
        #
        tags = MapiClient(s.url, s.creds).tags
        for t in tags:
            tags.delete(t)

    def test_tags(s):
        tags = MapiClient(s.url, s.creds).tags
        s.assertIsNotNone(tags)

        # When we are starting out there shouldn't be any tags currently defined
        # on the MAAS server.
        #
        s.assertEqual(len(tags), 0)

        # Verify we can add a tag
        #
        tags.add(Tag(name='intel-gpu', comment='Machines which have an Intel display driver', definition='contains(//node[@id="display"]/vendor, "Intel")'))
        s.assertEqual(len(tags), 1)

        # Verify we can delete the tag that we just added.
        #
        tags.delete(Tag(name='intel-gpu', comment='Machines which have an Intel display driver', definition='contains(//node[@id="display"]/vendor, "Intel")'))
        s.assertEqual(len(tags), 0)

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TagsTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
