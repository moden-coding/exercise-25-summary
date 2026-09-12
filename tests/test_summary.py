#!/usr/bin/env python3

import contextlib
import io
import sys
import unittest
from unittest.mock import patch
from itertools import repeat

from src.summary import summary, main


class Summary(unittest.TestCase):

    def test_one(self):
        s, a, d = summary("src/example.txt")
        self.assertAlmostEqual(
            s, 51.400000, places=4,
            msg="summary('src/example.txt') should return a sum of 51.4.")
        self.assertAlmostEqual(
            a, 10.280000, places=4,
            msg="summary('src/example.txt') should return an average of "
            "10.28.")
        self.assertAlmostEqual(
            d, 8.904606, places=4,
            msg="summary('src/example.txt') should return a population "
            "standard deviation of about 8.904606.")

    def test_two(self):
        s, a, d = summary("src/example2.txt")
        self.assertAlmostEqual(
            s, 5446.200000, places=4,
            msg="summary('src/example2.txt') should return a sum of "
            "5446.2.")
        self.assertAlmostEqual(
            a, 1815.400000, places=4,
            msg="summary('src/example2.txt') should return an average of "
            "1815.4.")
        self.assertAlmostEqual(
            d, 3124.294045, places=4,
            msg="summary('src/example2.txt') should return a population "
            "standard deviation of about 3124.294045.")

    def test_three(self):
        s, a, d = summary("src/example3.txt")
        self.assertAlmostEqual(
            s, 0.000000, places=4,
            msg="summary('src/example3.txt') should return a sum of 0.")
        self.assertAlmostEqual(
            a, 0.000000, places=4,
            msg="summary('src/example3.txt') should return an average of "
            "0.")
        self.assertAlmostEqual(
            d, 50.000000, places=4,
            msg="summary('src/example3.txt') should return a population "
            "standard deviation of about 50.0, even though the average is "
            "0 (the numbers cancel out but still vary).")

    def test_missing_file(self):
        with self.assertRaises(
                FileNotFoundError,
                msg="summary('doesnotexist') should let FileNotFoundError "
                "propagate instead of catching it."):
            summary("doesnotexist")

    def test_calls(self):
        with patch('builtins.open', side_effect=open) as o:
            summary("src/example.txt")
            self.assertTrue(
                o.called,
                msg="summary must actually open the given file with the "
                "built-in open().")

    def test_main(self):
        orig_argv = sys.argv
        n = 7
        sys.argv[1:] = ["file%i" % i for i in range(n)]
        try:
            with patch('src.summary.summary',
                       side_effect=repeat((0.0, 0.0, 0.0))) as s:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    main()
                self.assertEqual(
                    s.call_count, n,
                    msg="main() should call summary() once per command "
                    "line argument (expected %i calls for %i arguments)."
                    % (n, n))
            result = buf.getvalue().strip().split('\n')
            for i, line in enumerate(result):
                self.assertEqual(
                    line.strip(),
                    "File: file%i Sum: 0.000000 Average: 0.000000 "
                    "Stddev: 0.000000" % i,
                    msg="main() printed the wrong line for file%i when "
                    "summary() returns (0.0, 0.0, 0.0)." % i)
        finally:
            sys.argv = orig_argv


if __name__ == '__main__':
    unittest.main()
