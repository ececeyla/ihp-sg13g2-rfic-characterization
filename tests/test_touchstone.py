"""Deterministic tests: test-only data, not report measurements."""
import sys
from pathlib import Path
import tempfile
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from analyze_touchstone import read_touchstone, checks, analyze
from run_auto_nport_interactive import save_touchstone


class TouchstoneTests(unittest.TestCase):
    def test_two_port_column_major_and_db(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'test.s2p'
            p.write_text('# GHz S DB R 50\n10 -20 0 -6 0 -40 0 -10 0\n', encoding='ascii')
            f, s, z0 = read_touchstone(p)
            self.assertAlmostEqual(f[0], 1e10)
            self.assertEqual(z0, 50.)
            self.assertAlmostEqual(abs(s[0, 1, 0]), 10**(-6/20))
            self.assertAlmostEqual(abs(s[0, 0, 1]), .01)
            result = analyze(p, 10, Path(d)/'analysis', make_plots=False)
            self.assertEqual(result['nports'], 2)
            self.assertTrue((Path(d)/'analysis'/'summary.json').exists())

    def test_three_port_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'test.s3p'
            s = np.zeros((2, 3, 3), dtype=complex)
            s[:, 0, 1] = .3 + .1j
            s[:, 1, 0] = .2 - .1j
            save_touchstone(p, np.array([1e9, 2e9]), s, 50.)
            freq, parsed, z0 = read_touchstone(p)
            np.testing.assert_allclose(parsed, s)
            np.testing.assert_allclose(freq, [1e9, 2e9])
            self.assertEqual(z0, 50.)
            top_singular, asym = checks(parsed)
            self.assertTrue(np.all(top_singular <= 1))
            self.assertTrue(np.all(asym > 0))

    def test_malformed_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'bad.s3p'
            p.write_text('# Hz S RI R 50\n1 1 0\n')
            with self.assertRaises(ValueError):
                read_touchstone(p)

    def test_synthetic_fixture_is_parseable_but_not_historical_data(self):
        fixture = Path(__file__).resolve().parents[1] / 'examples' / 'synthetic_two_port_TEST_ONLY.s2p'
        freq, matrix, z0 = read_touchstone(fixture)
        np.testing.assert_allclose(freq / 1e9, [8.0, 10.0, 12.0])
        self.assertEqual(matrix.shape, (3, 2, 2))
        self.assertEqual(z0, 50.0)
        np.testing.assert_allclose(matrix[0, 1, 0], .8 - .1j)
        values, _ = checks(matrix)
        self.assertTrue(np.all(values < 1.0))

    def test_bad_frequency_order_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'decreasing.s1p'
            p.write_text('# GHz S RI R 50\n10 0.2 0\n8 0.2 0\n')
            with self.assertRaises(ValueError):
                read_touchstone(p)


if __name__ == '__main__':
    unittest.main()
