import unittest
import cffi.verifier
from kfreader import KFReader


class TestKFReader(unittest.TestCase):
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

    def test_non_existent_variable(self):
        with self.assertRaises(RuntimeError):
            self.kfr.get_data('does not', 'exist')

    def tearDown(self):
        self.kfr.close()
