# coding: utf-8
import pandas as pd

from nose.tools import assert_equals
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
        test_soya = Soya(
            engine=self.test_engine,
            input_dict={'table0': ['num1', ]}
        )
        print test_soya._datum_import()

        assert_equals(
            test_soya._datum_import(),
            {'table0': pd.DataFrame({'num1': [7, 8, 9]})}
        )
