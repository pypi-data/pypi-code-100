"""Channel test module"""

import sys
import unittest
import uuid
from matatika.channel import Channel

sys.path.append('../src/')


class TestChannel(unittest.TestCase):
    """Test class for channel operations"""

    def test_channel_attrs(self):
        """Test channel attributes"""

        channel = Channel()

        self.assertIsNone(channel.name)
        self.assertIsNone(channel.description)
        self.assertIsNone(channel.picture)

        name = 'channel'
        description = 'channel description'
        picture = '<><'

        channel.name = name
        channel.description = description
        channel.picture = picture

        self.assertEqual(channel.name, name)
        self.assertEqual(channel.description, description)
        self.assertEqual(channel.picture, picture)

    def test_to_dict_all_attrs(self):
        """Tests to_dict behaviour with all attributes"""

        channel = Channel()
        channel.name = 'channel'
        channel.description = 'channel description'
        channel.picture = '<><'

        channel_dict = {
            'name': channel.name,
            'description': channel.description,
            'picture': channel.picture
        }

        self.assertDictEqual(channel.to_dict(), channel_dict)
    
    def test_from_dict_all_attrs(self):
        """Tests from_dict behaviour with all attributes"""

        channel_dict = {
            'name': 'channel',
            'description': 'channel description',
            'picture': '<><'
        }

        channel = Channel.from_dict(channel_dict)

        self.assertIsInstance(channel, Channel)
        self.assertEqual(channel.name, 'channel')
        self.assertEqual(channel.description, 'channel description')
        self.assertEqual(channel.picture, '<><')
