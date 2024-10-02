import unittest

from html_builder import extract_title

class TestExtractTitle(unittest.TestCase):
    
    def test_simple(self):
        title = extract_title('# Hola')

        self.assertEqual(title, "Hola")

    def test_complex(self):
        title = extract_title("""# Hola

quipa

>shoro
`code`
""")

        self.assertEqual(title, "Hola")

    def test_wrong(self):
        md = """Hola

quipa

>shoro
`code`
"""

        with self.assertRaises(Exception):
            title = extract_title(md)

if __name__ == "__main__":
    unittest.main()
