# coding: utf8
import unittest


def readFile(path):
    content_file = open(path, 'r')
    content = content_file.read()
    return content

# unicode ascii oracle (decoded utf-8)
oracle_ascii = u'c\'est une plaisir  d\'écrire du python  £ - ¢ - § - €'

#unicode encoded oracle
unicode_oracle = oracle_ascii.encode('utf-8')
unicode_windows1252 = oracle_ascii.encode('cp1252')
unicode_iso855915 = oracle_ascii.encode('ISO-8859-15')
# ISO-8859-1 does not support the euro symbol, note the errors='ignore'
unicode_iso85591 = oracle_ascii.encode('ISO-8859-1', 'ignore')

class TransformEncoding:
    def __init__(self):
        self.content = None

    def set_content(self, content):
        self.content = content

    def latin1_to_iso855915(self):
        windows1252_text = self.content.decode('latin1')  # decode windows 1252 to ascii
        iso885915_text = windows1252_text.encode('ISO-8859-15')  # encode to ISO-8859-1
        return iso885915_text

    def windows1252_to_iso855915(self):
        windows1252_text = self.content.decode('cp1252')  # decode windows 1252 to ascii
        iso885915_text = windows1252_text.encode('ISO-8859-15')  # encode to ISO-8859-1
        return iso885915_text

    def windows1252_to_iso85591(self):
        windows1252_text = self.content.decode('cp1252')  # decode windows 1252 to ascii
        iso88591_text = windows1252_text.encode('ISO-8859-1')  # encode to ISO-8859-1
        return iso88591_text

    def utf8_to_iso85591(self):
        utf8_text = self.content.decode('utf8')  # decode windows 1252 to ascii
        iso88591_text = utf8_text.encode('ISO-8859-1')  # encode to ISO-8859-1
        return iso88591_text

    def utf8_to_iso855915(self):
        utf8_text = self.content.decode('utf8')  # decode windows 1252 to ascii
        iso885915_text = utf8_text.encode('ISO-8859-15')  # encode to ISO-8859-1
        return iso885915_text


class PythonEncodingTest(unittest.TestCase):
    def setUp(self):
        self.transformEncoding = TransformEncoding()

    # reading iso-855915
    def test_iso855915(self):
        content = readFile('../text-ISO885915.txt')

        self.assertEqual(unicode_iso855915, content)

        iso885915_text_ascii = content.decode('ISO-8859-15')  # decode ISO-8859-1 to ascii

        # the ascii representation of both should be surprisingly equal
        self.assertEqual(oracle_ascii, iso885915_text_ascii)

        utf8_text = iso885915_text_ascii.encode('utf-8')

        self.assertEqual(unicode_oracle, utf8_text)

    # reading iso-8559-1
    # no euro symbol in iso-8559-1
    # http://en.wikipedia.org/wiki/ISO_8859-1
    def test_iso85591(self):
        content = readFile('../text-ISO88591.txt')

        self.assertEqual(unicode_iso85591, content)

        iso88591_text_ascii = content.decode('ISO-8859-1')  # decode ISO-8859-1 to ascii

        # the ascii representation of ISO-8859-1 should not be equal to the ascii representation of utf-8
        self.assertNotEqual(oracle_ascii[0:55], iso88591_text_ascii[0:55])

        utf8_text = iso88591_text_ascii.encode('utf-8')  # encode ascii to utf-8

        # these should not be equal because ISO-8859-1 does not support the euro symbol
        self.assertNotEqual(unicode_oracle, utf8_text)

        # both utf-8 strings should be equals if we remove the euro symbol
        self.assertEqual(unicode_oracle[0:55], utf8_text[0:55])

    # reading windows-1252 -- otherwise known as ANSI
    def read_windows1252(self):
        content = readFile('../text-windows1252.txt')

        self.assertEqual(unicode_windows1252, content)

        windows1252_text_ascii = content.decode('cp1252')  # decode windows 1252 to ascii

        # the ascii representation of both should not be equal
        self.assertNotEqual(oracle_ascii, windows1252_text_ascii)

        utf8_text = windows1252_text_ascii.encode('utf-8')

        self.assertEqual(unicode_oracle, utf8_text)


    # Reading utf-8
    def test_utf8(self):
        content = readFile('../text-utf8.txt')

        # utf-8 content of both strings should be equal
        self.assertEqual(unicode_oracle, content)

        utf8_text_ascii = content.decode('utf-8')  # decode unicode to ascii
        # ascii content of both strings should be equal
        self.assertEqual(oracle_ascii, utf8_text_ascii)

    # read windows-1252 as latin1 and then transform to iso-8859-15
    def read_windows1252_as_latin1_to_iso855915(self):
        content = readFile('../text-windows1252.txt')

        self.transformEncoding.set_content(content)

        iso885915 = self.transformEncoding.latin1_to_iso855915()

        iso885915_oracle = oracle_ascii.encode('ISO-8859-15')

        # utf-8 ascii encoded to iso-8559-15 should be equals to iso-8859-15
        self.assertEqual(iso885915_oracle, iso885915)

    # read windows-1252 and then transform to iso-8859-15
    def test_windows1252_to_iso855915(self):
        content = readFile('../text-windows1252.txt')

        self.transformEncoding.set_content(content)

        iso885915 = self.transformEncoding.windows1252_to_iso855915()

        iso885915_oracle = oracle_ascii.encode('ISO-8859-15')

        # utf-8 ascii encoded to iso-8559-15 should be equals to iso-8859-15
        self.assertEqual(iso885915_oracle, iso885915)

    # read windows-1252 and then transform to iso-8859-1
    def test_windows1252_to_iso85591(self):
        content = readFile('../text-windows1252.txt')

        self.transformEncoding.set_content(content)

        # should raise an encode error exception to encode due 'latin-1' codec can't encode character u'\u20ac'
        self.assertRaises(UnicodeEncodeError, self.transformEncoding.windows1252_to_iso85591)

    # read utf-8 as latin1 and then transform to iso-8859-15
    def read_utf8_to_iso855915(self):
        content = readFile('../text-utf8.txt')

        self.transformEncoding.set_content(content)

        iso885915_text = self.transformEncoding.utf8_to_iso855915()

        iso885915_oracle = oracle_ascii.encode('ISO-8859-15')

        # utf-8 ascii encoded to iso-8559-15 should be equals to iso-8859-15
        self.assertEqual(iso885915_oracle, iso885915_text)


    def test_utf8_to_iso85591(self):
        content = readFile('../text-utf8.txt')

        self.transformEncoding.set_content(content)

        # should raise an encode error exception to encode due 'latin-1' codec can't encode character u'\u20ac'
        self.assertRaises(UnicodeEncodeError, self.transformEncoding.utf8_to_iso85591)

if __name__ == '__main__':
    unittest.main()