# coding: utf-8

import pandas as pd

class Soya(object):
    def __init__(self, input_dict, engine):
        self.engine = engine
        self.input_dict= input_dict

    def _datum_import(self):
        datum = {}
        for table, fields in self.input_dict.items():
            datum[table] = pd.read_sql('sql', self.engine, chunksize=)
        return datum

    def model(self, datum):
        # main cal
        return result

    def _datum_export(self, result, out_name):
        result.to_sql(self.engine, out_name)

    def run(self, out_name):
        datum = self._datum_import()
        self.datum_export(self.model(datum), out_name)

