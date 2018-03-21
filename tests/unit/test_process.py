#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: tests/unit/test_process.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 19.03.2018
from nose.tools import assert_equals

from soya import Soya


class TestSoya(Soya):
    """Child class of Soya to test
    """
    def model(self, model):
        return None


def test_Soya_init():
    """Check if `Soya.__init__` works
    """
    model = TestSoya(
        engine='test', input_dict={'test': ['test']}, read_chunksize=6
    )

    assert_equals(model.engine, 'test')
    assert_equals(model.input_dict, {'test': ['test']})
    assert_equals(model.read_chunksize, 6)
    assert_equals(model.write_chunksize, None)
