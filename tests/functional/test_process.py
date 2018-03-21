# coding: utf-8
import pandas as pd

from sqlalchemy import create_engine

from soya import Soya

class Soya1(Soya):
    """
    """
    def model(self, datum):
        num1 = datum['talbe1']['num1'].sum() + datum['talbe1']['num2'].sum()
        num2 = datum['talbe2']['num1'].sum()
        return pd.DataFrame({
            'num': [num1, num2]
        })

class TestRun(object):
    """Functional test class for ``Soya._datum_import``
    """
    def setUp(self):
        self.test_engine = create_engine(
            'mysql+mysqldb://root:password@mysql:3306/soya_test?charset=utf8',
            echo=False, encoding='utf8'
        )
        pd.DataFrame({'num1': [1, 2, 3], 'num2': [4, 5, 6]}).to_sql(
            name='table1', con=self.test_engine,
            if_exists='replace', index=False
        )
        pd.DataFrame({'num1': [7, 8, 9]).to_sql(
            name='table2', con=self.test_engine,
            if_exists='replace', index=False
        )

    def test_soya_run_no_chunk(self):
        """Check if `Soya.run` works with no chunksize
        """
        test_soya = Soya1(
            engine=self.test_engine,
            input_dict={'table1': ['num1', 'num2'], 'table2': ['num1']}
        )
        expect_results = {'table_result': pd.DataFrame({'num': [21, 24]})}

        test_soya.run('table_result')

        results = pd.read_sql('select num from table_result', self.test_engine) # todo

        pd.testing.assert_frame_equal(expect_results['table_result'], results)

#    def test_soya_datum_import_chunk(self):
#        """Check if `_datum_import` works with chunksize
#        """
#        test_soya = Soya(
#            engine=self.test_engine,
#            input_dict={'table0': ['num1', ]},
#            read_chunksize=2
#        )
#        expect_results = {
#            'table0': [
#                pd.DataFrame({'num1': [7, 8]}),
#                pd.DataFrame({'num1': [9, ]})
#            ]
#        }
#        results = test_soya._datum_import()
#
#        for key, expect_values in expect_results.items():
#            for expect_value, value in zip(expect_values, results[key]):
#                pd.testing.assert_frame_equal(expect_value, value)
