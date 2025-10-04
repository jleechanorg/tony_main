import unittest
import struct
from io import BytesIO


class TestTurboRealDecoder(unittest.TestCase):
    """Test cases for Turbo Pascal Real48 decoder"""

    def test_decode_zero(self):
        """Test that exponent=0 returns -1 (no mark indicator)"""
        from marks_reader import decode_turbo_real
        # Exponent byte = 0 means zero/no mark
        bytes_data = b'\x00\x00\x00\x00\x00\x00'
        result = decode_turbo_real(bytes_data)
        self.assertEqual(result, -1.0)

    def test_decode_positive_number(self):
        """Test decoding a positive number"""
        from marks_reader import decode_turbo_real
        # Test with known value: 17.0
        # We can verify this against the CSV data we know is correct
        # For now, test the structure is valid
        bytes_data = b'\x84\x10\x00\x00\x00\x00'  # Example bytes
        result = decode_turbo_real(bytes_data)
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)

    def test_decode_invalid_length(self):
        """Test that wrong length returns None"""
        from marks_reader import decode_turbo_real
        bytes_data = b'\x00\x00\x00'  # Only 3 bytes
        result = decode_turbo_real(bytes_data)
        self.assertIsNone(result)

    def test_mantissa_leading_one(self):
        """Test that mantissa includes implicit leading 1"""
        from marks_reader import decode_turbo_real
        # This is the critical fix - mantissa should be (1.m) not just (m)
        # A simple test: if mantissa bits are all zero, value should be 1.0 * 2^(exp-129)
        # exp = 129 means 2^0 = 1.0
        bytes_data = b'\x81\x00\x00\x00\x00\x00'  # exp=129, mantissa=0, positive
        result = decode_turbo_real(bytes_data)
        self.assertAlmostEqual(result, 1.0, places=5)


class TestPascalStringReader(unittest.TestCase):
    """Test cases for Pascal string reader"""

    def test_read_simple_string(self):
        """Test reading a simple Pascal string"""
        from marks_reader import read_pascal_string
        # Pascal string: length byte + characters
        # "ABC" = 0x03 + "ABC" + padding
        data = BytesIO(b'\x03ABC' + b' ' * 17)  # Length 3 + "ABC" + padding to 20
        result = read_pascal_string(data, 20)
        self.assertEqual(result, 'ABC')

    def test_read_empty_string(self):
        """Test reading an empty Pascal string"""
        from marks_reader import read_pascal_string
        data = BytesIO(b'\x00' + b' ' * 20)
        result = read_pascal_string(data, 20)
        self.assertEqual(result, '')

    def test_read_full_length_string(self):
        """Test reading a string at max length"""
        from marks_reader import read_pascal_string
        name = "CHAN BOBBY"
        data = BytesIO(bytes([len(name)]) + name.encode('latin-1') + b' ' * (20 - len(name)))
        result = read_pascal_string(data, 20)
        self.assertEqual(result, name)


class TestStudentRecord(unittest.TestCase):
    """Test cases for student record reading"""

    def test_read_config_file(self):
        """Test reading the configuration file"""
        from marks_reader import read_config_file
        config = read_config_file(r'S:\Chn\classes\Ics4m1-1.txt')

        self.assertEqual(config['class_code'], 'ICS4M1-1')
        self.assertEqual(config['num_cat'], 5)
        self.assertEqual(config['num_marks'], 15)
        self.assertEqual(len(config['categories']), 5)
        self.assertEqual(len(config['marks']), 15)

        # Verify first assignment
        self.assertEqual(config['marks'][0]['name'], 'A1')
        self.assertEqual(config['marks'][0]['total'], 20.0)

    def test_format_mark(self):
        """Test mark formatting"""
        from marks_reader import format_mark

        self.assertEqual(format_mark(17.0), '17.0')
        self.assertEqual(format_mark(8.5), '8.5')
        self.assertEqual(format_mark(-1.0), '')  # No mark
        self.assertEqual(format_mark(999.0), '')  # No mark
        self.assertEqual(format_mark(17.123), '17.1')  # Should round to 1 decimal


class TestCSVConversion(unittest.TestCase):
    """Test cases for CSV conversion"""

    def test_convert_class_to_csv(self):
        """Test converting a class file to CSV"""
        from marks_reader import convert_class_to_csv

        rec_file = r'S:\Chn\classes\Ics4m1-1.rec'
        txt_file = r'S:\Chn\classes\Ics4m1-1.txt'
        output_dir = r'S:\Chn\classes\csv_exports_python'

        result = convert_class_to_csv(rec_file, txt_file, output_dir)

        self.assertIsNotNone(result)
        self.assertEqual(result['class_code'], 'ICS4M1-1')
        self.assertEqual(result['num_students'], 14)
        self.assertEqual(result['num_marks'], 15)


if __name__ == '__main__':
    unittest.main()
