#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: soya/process.py
# Author: Jimin Huang <huangjimin@whu.edu.cn>
# Date: 19.03.2018

import pandas as pd


class Soya(object):
    """The abstract class for implementing the process.

    The class provides a interface `Soya.model` to implement the process, whose
    required parameters is given from `__init__`.

    The class initializes with following parameters:
        engine: a `Sqlalchemy.engine` to provide database connection
        input_dict: a dict of {`table_name`: a list of `table_field`}
        read_chunk_size: an `int`, the chunk size of reading datum from
        database, default is None
        write_chunk_size: an `int`, the chunk size of writing result to
        database.
    """
    def __init__(
        self, engine, input_dict, read_chunk_size=None, write_chunk_size=None
    ):
        self.engine = engine
        self.input_dict = input_dict
        self.read_chunk_size = read_chunk_size
        self.write_chunk_size = write_chunk_size

    def _datum_import(self, input_dict, read_chunksize):
        """import datumn from sql

        Args:
            input_dict: a dict of {`table_name`: a list of `table_field`}
            read_chunk_size: an `int`, the chunk size of reading datum from
        """
        return {
            tablename: pd.read_sql(
                'select {0} from {1}'.format(','.join(fields), tablename),
                self.engine, chunksize=self.read_chunk_size
            ) for tablename, fields in input_dict
        }
