import os.path
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))
from plugins.generic import (
    unpack_source_url,
    unpack_source_url_re_1,
    unpack_source_url_re_2,
    unpack_source_url_re_3,
) # noqa


class TestPluginResolve(unittest.TestCase):
    def test_unpack_source_atob(self):
        # unpack_source_url_re_1
        self.assertEqual(unpack_source_url("""
            var player = new Clappr.Player(
            player.attachTo(playerElement);
            player.load({source: window.atob('aHR0cHM6Ly9leGFtcGxlLmNvbQ=='), mimeType: 'application/vnd.apple.mpegurl'});
            """, unpack_source_url_re_1), """
            var player = new Clappr.Player(
            player.attachTo(playerElement);
            player.load({source: 'https://example.com', mimeType: 'application/vnd.apple.mpegurl'});
            """)

    def test_unpack_source_atob2(self):
        self.assertEqual(unpack_source_url("""
            var player = new Clappr.Player(
            player.attachTo(playerElement);
            player.load({source: window.atob("aHR0cHM6Ly9leGFtcGxlLmNvbQ=="), mimeType: "application/vnd.apple.mpegurl"});
            """, unpack_source_url_re_1), """
            var player = new Clappr.Player(
            player.attachTo(playerElement);
            player.load({source: "https://example.com", mimeType: "application/vnd.apple.mpegurl"});
            """)

    def test_unpack_source_atob3(self):
        # unpack_source_url_re_2
        self.assertEqual(unpack_source_url("""
            var xurl=atob('aHR0cHM6Ly9leGFtcGxlLmNvbQ==');
            player=new Clappr.Player
            """, unpack_source_url_re_2), """
            var xurl='https://example.com';
            player=new Clappr.Player
            """)

    def test_unpack_source_atob_fail(self):
        # INVALID unpack_source_url
        self.assertEqual(unpack_source_url("""
            var xurl=atob('xxx=');
            player=new Clappr.Player
            """, unpack_source_url_re_2), """
            var xurl='INVALID unpack_source_url';
            player=new Clappr.Player
            """)

    def test_unpack_source_atob4(self):
        self.assertEqual(unpack_source_url("""
            var player = new Clappr.Player({
            source: atob('aHR0cHM6Ly9leGFtcGxlLmNvbQ=='),
            """, unpack_source_url_re_3), """
            var player = new Clappr.Player({
            source: 'https://example.com',
            """)
