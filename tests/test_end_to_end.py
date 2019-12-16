from unittest import TestCase
import filecmp
import pandas as pd
import os.path as osp
import os
from shared_test_data import test_csv_filepath, test_asc_filepath

import writer
import reader
import main

args = {
    'in_format': 'csv',
    'out_format': 'csv',
    'in_data_file': '',
    'out_data_file': 'tmp.tmp',
    'student_column': 'user_id',
    'skill_column': 'skill_id',
    'correct_column': 'correct'
}


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        os.mkdir('tmp')

    @classmethod
    def tearDownClass(cls):
        os.rmdir('tmp')

    def from_csv_equals_to_csv(self):
        main.run(args)
        self.assertEqual(pd.read_csv(args['in_data_file']), pd.read_csv(args['out_data_file']))

    def from_asc_equals_to_asc(self):
        test_args = args
        test_args['in_data_file'] = 'data/test.asc'
        test_args['in_format'] = 'asc'
        test_args['out_format'] = 'asc'
        main.run(test_args)

        self.assertTrue(filecmp.cmpfiles(test_args['in_data_file'], test_args['out_data_file']))
