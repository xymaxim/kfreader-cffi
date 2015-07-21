from unittest import TestCase
from unittest.mock import patch

import cffi.verifier

from kfreader import KFReader, KFFileReadingError, kfropen


class TestKFReader(TestCase):
    def setUp(self):
        cffi.verifier.cleanup_tmpdir()
        self.kfr = KFReader('tests/TAPE21')

    def test_double(self):
        x = self.kfr.get_data('Energy', 'Bond Energy')
        self.assertAlmostEqual(x, -0.1142717944)

    def test_double_array(self):
        x = self.kfr.get_data('Geometry', 'xyz')
        self.assertEqual(len(x), 6)
        self.assertNotEqual(x[2], 0)
        self.assertNotEqual(x[-1], 0)

    def test_string(self):
        x = self.kfr.get_data('General', 'runtype')
        self.assertEqual(x, 'GEOMETRY OPTIMIZATION')

    def test_logical(self):
        x = self.kfr.get_data('General', 'lhybrid')
        self.assertFalse(x, 0)

    def test_non_existent_variable(self):
        with self.assertRaises(RuntimeError):
            self.kfr.get_data('does not', 'exist')

    def test_contextmanager(self):
        with kfropen('tests/TAPE21') as kfr:
            assert kfr != None

    @patch('kfreader.KFReader.close')
    def test_raised_contextmanager(self, mock_close):
        with self.assertRaises(KFFileReadingError):
            with kfropen('nonexistent_file') as kfr:
                pass
        assert not mock_close.called

    def tearDown(self):
        self.kfr.close()


class TestInvalidFileInput(TestCase):
    def setUp(self):
        cffi.verifier.cleanup_tmpdir()
        self.kfr = KFReader()

    def test_non_existent_file(self):
        self.assertRaises(KFFileReadingError, self.kfr.open, '/does/not/exist')

    def test_unexpected_format(self):
        self.assertRaises(KFFileReadingError, self.kfr.open, 'tests/empty.txt')

    def tearDown(self):
        # self.kfr.close()
        pass
