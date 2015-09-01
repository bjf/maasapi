
from time                               import sleep
import unittest
from maasapi.client                     import MapiClient
from maasapi.tag                        import Tag
from maasapi_test_case                  import MAASApiTestCase

class TagTestCase(MAASApiTestCase):

    def tearDown(s):
        # Cleanup (delete) any tags that were created during testing.
        #
        tags = MapiClient(s.url, s.creds).tags
        for t in tags:
            tags.delete(t)

    def test_tag(s):

        mc = MapiClient(s.url, s.creds)
        tags = mc.tags
        s.assertIsNotNone(tags)

        # Add two tags and verify we can get them back.
        #
        tags.add(Tag(client=mc, name='intel-gpu', comment='Intel GPUs', definition='//node[@id="display"]/vendor = "Intel Corporation"'))
        tags.add(Tag(client=mc, name='intel-cpu', comment='Intel CPUs', definition='//node[@class="processor"]/vendor = "Intel Corp."'))
        sleep(1)            # Hack

        s.assertEqual(len(tags), 2)

        tag = tags[0]
        s.assertIsNotNone(tag)
        s.assertEqual(tag.name, 'intel-gpu')
        s.assertEqual(tag.comment, 'Intel GPUs')
        s.assertEqual(tag.definition, '//node[@id="display"]/vendor = "Intel Corporation"')

        tag = tags[1]
        s.assertIsNotNone(tag)
        s.assertEqual(tag.name, 'intel-cpu')
        s.assertEqual(tag.comment, 'Intel CPUs')
        s.assertEqual(tag.definition, '//node[@class="processor"]/vendor = "Intel Corp."')

        # On the MAAS server that I'm using for testing there are 2 Intel NUCs defined. Make
        # sure those both got tagged.
        #
        nodes = tag.nodes
        s.assertEqual(len(nodes), 2)
        s.assertIn(nodes[0]['hostname'], ['nuc1.maas', 'nuc2.maas'], msg='Expected \'nuc[12].maas\' but got \'%s\' instead.' % nodes[0]['hostname'])
        s.assertIn(nodes[1]['hostname'], ['nuc1.maas', 'nuc2.maas'], msg='Expected \'nuc[12].maas\' but got \'%s\' instead.' % nodes[1]['hostname'])

        # Run a rebuild on both tags just to see if anything blows up.
        #
        tags[0].rebuild()
        tags[1].rebuild()

        # Update the first tag and verify that it got updated.
        #
        tags[0].update(name='iNtEl-GpU', comment='This is a test')
        sleep(1)            # Hack
        tags = mc.tags      # Hack - The update operated on an individual tag but no way to mark the
                            #        internal s.__tags as dirty.
        s.assertEqual(tags[1].name, 'iNtEl-GpU')

        # Test adding and removing nodes from a tag.
        #
        tags = mc.tags
        tag = tags[0]
        nodes = tag.nodes
        print(tag.name)
        for n in nodes:
            print(n['system_id'])
        s.assertEqual(len(nodes), 2)
        tag.remove_nodes(nodes[0]['system_id'])
        sleep(1)            # Hack
        print('')
        tags = mc.tags
        tag = tags[0]
        print(tag.name)
        nodes = tag.nodes
        for n in nodes:
            print(n['system_id'])
        s.assertEqual(len(nodes), 1)

if __name__ == '__main__':
    unittest.main()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TagsTestCase)
    #unittest.TextTestRunner(verbosity=2).run(suite)
