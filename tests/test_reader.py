from unittest import TestCase
import pandas as pd

from shared_test_data import test_asc_filepath
from src import reader


class ReaderTest(TestCase):

    def test_read_asc(self):
        filepath = test_asc_filepath
        data = reader.read_asc(filepath, 'user_id', 'skill_id', 'correct')
        expected = pd.DataFrame({'user_id': [0, 0, 0, 1, 1, 1, 1, 1, 2, 2],
                                 'skill_id': [1, 2, 3, 3, 4, 2, 1, 0, 1, 1],
                                 'correct': [0, 0, 1, 0, 0, 0, 1, 1, 0, 1]})
        self.assertTrue(expected.equals(data[expected.columns]))
