import os.path
import sys
import unittest

sys.path.insert(0, os.path.abspath('..'))
from plugins.generic import UnpackingError, Packer, unpack_packer  # noqa


class TestPacker(unittest.TestCase):

    def setUp(self):
        self.my_unpacker = Packer()

    def test_detect(self):
        self.assertTrue(self.my_unpacker.detect('eval(function(p,a,c,k,e,r'))
        self.assertTrue(self.my_unpacker.detect('eval ( function(p, a, c, k, e, r'))

    def test_detect_false(self):
        self.assertFalse(self.my_unpacker.detect(''))
        self.assertFalse(self.my_unpacker.detect('var a = b'))

    def test_unpack(self):
        test_list = [
            ("eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String))"
             "{while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function"
             "(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp("
             "'\\b'+e(c)+'\\b','g'),k[c]);return p}('(0(){4 1=\"5 6 7 8\";0 2"
             "(3){9(3)}2(1)})();',10,10,'function|b|something|a|var|some|samp"
             "le|packed|code|alert'.split('|'),0,{}))",
             """(function(){var b="some sample packed code";"""
             """function something(a){alert(a)}something(b)})();"""),
            ("eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)"
             "){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e="
             "function(){return'\\\\w+'};c=1};while(c--)if(k[c])p=p.replace("
             "new RegExp('\\\\b'+e(c)+'\\\\b','g'),k[c]);return p}('0 2=1',"
             "62,3,'var||a'.split('|'),0,{}))",
             'var a=1'),
            ("""eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,Strin"""
             """g)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=fu"""
             """nction(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(ne"""
             """w RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('0="1://2.3/4"""
             """.5"',6,6,'var|http|example|com|test|m3u8'.split('|'),0,{}))""",
             'var="http://example.com/test.m3u8"'),
            ("""eval(function(p,a,c,k,e,d){e=function(c){return c};if(!''."""
             """replace(/^/,String)){while(c--){d[c]=k[c]||c}k=[function(e"""
             """){return d[e]}];e=function(){return'\\w+'};c=1};while(c--)"""
             """{if(k[c]){p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c"""
             """])}}return p}('0 1 2',3,3,'Test|Live|Stream'.split('|'),0,"""
             """{}))""", 'Test Live Stream'),
        ]
        for _text, _r in test_list:
            self.assertEqual(self.my_unpacker.unpack(_text), _r)

    def test_unpack_error(self):
        with self.assertRaises(UnpackingError):
            self.my_unpacker.unpack('eval(function(p,a,c,k,e,r){e=String;if')

    def test_unpack_radix_1(self):
        test_list = [
            ("eval(function(p,a,c,k,e,d){while(c--){if(k[c]){p=p.replace(new R"
             "egExp('\b'+c+'\b','g'),k[c])}}return p}('36 41=18('4');18('4').4"
             "2({38:37,17:[{5:'16://19.20.7:23/22/15/2.3',24:'2/3','10':'6'}],"
             "14:{11:12(){$('#4').13(8)}},9:{21:'25',34:'#33',35:0},32:'',30:'"
             "',26:'1%',27:'1%',17:[{5:'16://19.20.7:23/22/15/2.3',24:'2/3','1"
             "0':'6'}],14:{11:12(){$('#4').13(8)}},9:{21:'25',34:'#33',35:0},3"
             "2:'',30:'',26:'1%',27:'1%',45:'',28:{29:'31'},28:{29:'31'},47:{5"
             ":'',48:'43://49.7',46:6,40:'39-44'},});',1,50,'|100|video|mp4|al"
             "lplayer|file|true|com|googleplayer|captions|default|onError|func"
             "tion|html|events|session|https|sources|jwplayer|www|example|edge"
             "Style|d|282|type|uniform|height|width|skin|name|aboutlink|bekle|"
             "abouttext|FFFFFF|backgroundColor|backgroundOpacity|var|primaryCo"
             "okie|primary|top|position|playerInstance|setup|http|right|image|"
             "hide|logo|link|player'.split('|')))",
             "var playerInstance=jwplayer('allplayer');jwplayer('allplayer').s"
             "etup({primary:primaryCookie,sources:[{file:'https://www.example."
             "com:282/d/session/video.mp4',type:'video/mp4','default':'true'}]"
             ",events:{onError:function(){$('#allplayer').html(googleplayer)}}"
             ",captions:{edgeStyle:'uniform',backgroundColor:'#FFFFFF',backgro"
             "undOpacity:0},abouttext:'',aboutlink:'',height:'100%',width:'100"
             "%',sources:[{file:'https://www.example.com:282/d/session/video.m"
             "p4',type:'video/mp4','default':'true'}],events:{onError:function"
             "(){$('#allplayer').html(googleplayer)}},captions:{edgeStyle:'uni"
             "form',backgroundColor:'#FFFFFF',backgroundOpacity:0},abouttext:'"
             "',aboutlink:'',height:'100%',width:'100%',image:'',skin:{name:'b"
             "ekle'},skin:{name:'bekle'},logo:{file:'',link:'http://player.com"
             "',hide:true,position:'top-right'},});"),
        ]
        for _text, _r in test_list:
            self.assertEqual(self.my_unpacker.unpack(_text), _r)

    def test_unpack_packer(self):
        self.assertEqual(unpack_packer("""
<html>
<head><title>Title of the document</title></head>
<body>
eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('<0 1="2://3.4"></0>',5,5,'iframe|src|https|example|com'.split('|'),0,{}))
</body></html>
"""), """
<html>
<head><title>Title of the document</title></head>
<body>
<iframe src="https://example.com"></iframe>
</body></html>
""")

    def test_unpack_packer_multiple(self):
        self.assertEqual(unpack_packer("""
<html>
<head><title>Title of the document</title></head>
<body>
eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('<0 1="2://3.4"></0>',5,5,'iframe|src|https|example1|com'.split('|'),0,{}))
eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('<0 1="2://3.4"></0>',5,5,'iframe|src|https|example2|com'.split('|'),0,{}))
eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('<0 1="2://3.4"></0>',5,5,'iframe|src|https|example3|com'.split('|'),0,{}))
</body>
eval(function(p,a,c,k,e,r){e=String;if(!''.replace(/^/,String)){while(c--)r[c]=k[c]||c;k=[function(e){return r[e]}];e=function(){return'\\w+'};c=1};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p}('<0 1="2://3.4"></0>',5,5,'iframe|src|https|example4|com'.split('|'),0,{}))
</html>
"""), """
<html>
<head><title>Title of the document</title></head>
<body>
<iframe src="https://example1.com"></iframe>
<iframe src="https://example2.com"></iframe>
<iframe src="https://example3.com"></iframe>
</body>
<iframe src="https://example4.com"></iframe>
</html>
""")
