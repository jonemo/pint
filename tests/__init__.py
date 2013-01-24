# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals, print_function, absolute_import

import sys
import logging
import unittest

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

PYTHON3 = sys.version >= '3'

if PYTHON3:
    string_types = str
    def u(x):
        return x
else:
    import codecs
    string_types = basestring
    def u(x):
        return codecs.unicode_escape_decode(x)[0]

from pint import logger, UnitRegistry

h = logging.StreamHandler()
f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
h.setLevel(logging.DEBUG)
h.setFormatter(f)
logger.addHandler(h)
logger.setLevel(logging.DEBUG)


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ureg = UnitRegistry(force_ndarray=cls.FORCE_NDARRAY)
        cls.Q_ = cls.ureg.Quantity

    def assertSequenceEqual(self, seq1, seq2, msg=None, seq_type=None):
        if isinstance(seq1, np.ndarray):
            seq1 = seq1.tolist()
        if isinstance(seq2, np.ndarray):
            seq2 = seq2.tolist()
        unittest.TestCase.assertSequenceEqual(self, seq1, seq2, msg, seq_type)

    def assertAlmostEqual(self, first, second, places=None, msg=None, delta=None):
        if isinstance(first, self.Q_) and isinstance(second, self.Q_):
            second = second.to(first)
            unittest.TestCase.assertAlmostEqual(self, first.magnitude, second.magnitude, places, msg, delta)
            self.assertEqual(first.units, second.units)
        elif isinstance(first, self.Q_):
            self.assertTrue(first.dimensionless)
            first = first.to('')
            unittest.TestCase.assertAlmostEqual(self, first.magnitude, second, places, msg, delta)
        elif isinstance(second, self.Q_):
            self.assertTrue(second.dimensionless)
            second = second.to('')
            unittest.TestCase.assertAlmostEqual(self, first, second.magnitude, places, msg, delta)
        else:
            unittest.TestCase.assertAlmostEqual(self, first, second, places, msg, delta)

