import unittest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))
import utility

class TestUtility(unittest.TestCase):

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        pass

    def test_snake2camel(self):
        assert utility.snake2camel("aha_uhu") == "ahaUhu"
        assert utility.snake2camel("aha") == "aha"
    
    def test_convert_key(self):
        assert utility.convert_key({"aha": {"hah": 2}}, lambda x: x.replace("a", "v")) == {"vhv": {"hvh": 2}}

if __name__ == '__main__':
    unittest.main()