# coding: utf-8
import pandas as pd

from sqlalchemy import create_engine

from soya import Soya


class TestDatumImport(object):
    """Integration test class for ``Soya._datum_import``
    """
    def setUp(self):
        self.test_engine = create_engine(
            'mysql+mysqldb://root:password@mysql:3306/soya_test?charset=utf8',
            echo=False, encoding='utf8'
        )
        pd.DataFrame({'num1': [7, 8, 9]}).to_sql(
            name='table0', con=self.test_engine,
            if_exists='replace', index=False
        )

    def test_soya_datum_import_no_chunk(self):
        """Check if `_datum_import` works with no chunksize
        """
        test_soya = Soya(
            engine=self.test_engine,
            input_dict={'table0': ['num1', ]}
        )
        expect_results = {'table0': pd.DataFrame({'num1': [7, 8, 9]})}
        results = test_soya._datum_import()

        for key, value in expect_results.items():
            assert value.equals(results[key])

    def test_soya_datum_import_chunk(self):
        """Check if `_datum_import` works with chunksize
        """
        test_soya = Soya(
            engine=self.test_engine,
            input_dict={'table0': ['num1', ]},
            read_chunksize=2
        )
        expect_results = {
            'table0': [
                pd.DataFrame({'num1': [7, 8]}),
                pd.DataFrame({'num1': [9,]})
            ]
        }
        results = test_soya._datum_import()

        for key, value in expect_results.items():
            assert value.equals(results[key])
