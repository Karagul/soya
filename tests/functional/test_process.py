# coding: utf-8
import pandas as pd

from itertools import tee
from sqlalchemy import create_engine

from soya import Soya


class Soya1(Soya):
    """Child class of Soya to rewrite the model
    """
    def model(self, datum):
        num1 = datum['table1']['num1'].sum() + datum['table1']['num2'].sum()
        num2 = datum['table2']['num1'].sum()
        return pd.DataFrame({
            'num': [num1, num2]
        })


class Soya2(Soya):
    """Child class 2 of Soya to rewrite the model
    """
    def model(self, datum):
        datum, datum_copy = tee(datum)
        num1 = sum(
            [
                (
                    datum_chunk['table1']['num1'].sum() +
                    datum_chunk['table1']['num2'].sum()
                ) for datum_chunk in datum
            ]
        )
        num2 = sum(
            [
                datum_chunk['table2']['num1'].sum()
                for datum_chunk in datum_copy
            ]
        )
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
        pd.DataFrame({'num1': [7, 8, 9]}).to_sql(
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

        results = pd.read_sql('select num from table_result', self.test_engine)

        pd.testing.assert_frame_equal(expect_results['table_result'], results)

    def test_soya_run_write_chunk(self):
        """Check if `Soya.run` works with write chunksize
        """
        test_soya = Soya1(
            engine=self.test_engine,
            input_dict={'table1': ['num1', 'num2'], 'table2': ['num1']},
            write_chunksize=1
        )
        expect_results = {'table_result': pd.DataFrame({'num': [21, 24]})}

        test_soya.run('table_result1')

        results = pd.read_sql('select num from table_result', self.test_engine)

        pd.testing.assert_frame_equal(expect_results['table_result'], results)

    def test_soya_run_read_chunk(self):
        """Check if `Soya.run` works with read chunksize
        """
       test_soya = Soya2(
            engine=self.test_engine,
            input_dict={'table1': ['num1', 'num2'], 'table2': ['num1']},
            read_chunksize=2
        )
        expect_results = {'table_result': pd.DataFrame({'num': [21, 24]})}

        test_soya.run('table_result2')

        results = pd.read_sql('select num from table_result', self.test_engine)

        pd.testing.assert_frame_equal(expect_results['table_result'], results)
