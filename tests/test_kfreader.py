import unittest
import cffi.verifier
from kfreader import KFReader


class TestKFReader(unittest.TestCase):
    def setUp(self):
        cffi.verifier.cleanup_tmpdir()
        self.kfr = KFReader('tests/TAPE21')

    def test_double(self):
        x = self.kfr.get_data('Energy', 'Bond Energy')
        self.assertAlmostEqual(x, -0.11427179)

    def test_double_array(self):
        x = self.kfr.get_data('Geometry', 'xyz')
        self.assertEqual(len(x), 6)
        self.assertNotEqual(x[2], 0)
        self.assertNotEqual(x[-1], 0)


    def test_string(self):
        x = self.kfr.get_data('General', 'runtype')
        self.assertEqual(x, 'GEOMETRY OPTIMIZATION')

    def tearDown(self):
        self.kfr.close()
