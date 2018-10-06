import os.path
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))
from plugins.generic import unpack_unescape  # noqa


class TestPacker(unittest.TestCase):

    def test_unpack_unescape(self):
        self.assertEqual(unpack_unescape("""
<html>
<head><title>Title of the document</title></head>
<body>
<script>
document.write(unescape("Live%20Test%20unescape"));
</script>
</body></html>
"""), """
<html>
<head><title>Title of the document</title></head>
<body>
Live Test unescape
</body></html>
""")

    def test_unpack_unescape_normal(self):
        self.assertEqual(unpack_unescape("""<script type="text/javascript">document.write(unescape('Test%201'));</script>"""),
                         "Test 1")

    def test_unpack_unescape_newline(self):
        self.assertEqual(unpack_unescape("""
<script type="text/javascript">
document.write(unescape('Test%202'));
</script>"""), "\nTest 2")

    def test_unpack_unescape_uncommented(self):
        self.assertEqual(unpack_unescape("""
<script type="text/javascript">
<!--
document.write(unescape('Test%203'));
//-->
</script>"""), "\nTest 3")

    def test_unpack_unescape_multiple(self):
        self.assertEqual(unpack_unescape("""
<html>
<head><title>Title of the document</title></head>
<body>
<script>
document.write(unescape("%3Cscript%3E%0Adocument.write%28unescape%28%22Test%2520Script%22%29%29%3B%0A%3C/script%3E"));
</script>
</body></html>
"""), """
<html>
<head><title>Title of the document</title></head>
<body>
Test Script
</body></html>
""")
