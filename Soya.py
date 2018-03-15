# coding: utf-8

import pandas as pd

class Soya(object):
    def __init__(self, input_dict, engine):
        self.input_dict = input_dict
        self.data = None
        self.engine = engine
        self.result = None
        for table in input_dict.keys():
            # make table name to be an attr like 'self.data.stocks'

    def data_import(self):
        for table, fields in self.input_dict.items():
            self.data.table = pd.read_sql('sql', self.engine, chunksize=)

    def model(self):
        # main cal
        self.result.names = ...
        self.result.fields = ...
        self.result.data = ...


    def data_export(self):
        pass
        self.result.data.to_sql(self.result.name, self.engine)

    def run(self):
        self.data_import()
        self.model()
        self.data_export()

