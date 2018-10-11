import unittest

from plugins.generic import unpack_source_url


class TestPluginResolve(unittest.TestCase):
    def test_unpack_source_atob(self):
        self.assertEqual(unpack_source_url("""
            var player = new Clappr.Player(
            player.attachTo(playerElement);
            player.load({source: window.atob('aHR0cHM6Ly9leGFtcGxlLmNvbQ=='), mimeType: 'application/vnd.apple.mpegurl'});
            """), """
            var player = new Clappr.Player(
            player.attachTo(playerElement);
            player.load({source: 'https://example.com', mimeType: 'application/vnd.apple.mpegurl'});
            """)
        self.assertEqual(unpack_source_url("""
            var player = new Clappr.Player(
            player.attachTo(playerElement);
            player.load({source: window.atob("aHR0cHM6Ly9leGFtcGxlLmNvbQ=="), mimeType: "application/vnd.apple.mpegurl"});
            """), """
            var player = new Clappr.Player(
            player.attachTo(playerElement);
            player.load({source: "https://example.com", mimeType: "application/vnd.apple.mpegurl"});
            """)
