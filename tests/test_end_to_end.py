from unittest import TestCase
import filecmp
import pandas as pd
import shutil
import os

from shared_test_data import test_csv_filepath, test_asc_filepath, dict_to_obj

import main
import conf

tmpdir = 'tmp_test'
args = {k: v['default'] for k, v in conf.args_map.items()}
args['in_data_file'] = 'data/assistments2009-skill-builders-corrected_1000.csv'
args['out_data_file'] = tmpdir + '/tmp.tmp'
args['in_format'] = 'csv'
args['out_format'] = 'csv'


class EndToEndTest(TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(tmpdir): os.mkdir(tmpdir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tmpdir)  # Remove this to check created files

    def test_from_csv_equals_to_csv(self):
        test_args = args.copy()
        test_args['out_data_file'] = tmpdir + '/tmp.csv'
        main.run(dict_to_obj(test_args))

        expected = pd.read_csv(test_args['in_data_file'])
        created = pd.read_csv(test_args['out_data_file'])
        self.assertTrue(expected.equals(created))

    def test_from_asc_equals_to_asc(self):
        test_args = args.copy()
        test_args['in_data_file'] = 'data/test.asc'
        test_args['out_data_file'] = tmpdir + '/tmp.asc'
        test_args['in_format'] = 'asc'
        test_args['out_format'] = 'asc'
        main.run(dict_to_obj(test_args))

        self.assertTrue(filecmp.cmp(test_args['in_data_file'], test_args['out_data_file']))

    def test_train_test_split_creates_train_and_test_files(self):
        test_args = args.copy()
        test_args['train_test_split'] = 0.2
        test_args = dict_to_obj(test_args)

        original_data_len = len(pd.read_csv(test_args.in_data_file))
        train_data_expected_len = int(original_data_len * (1 - test_args.train_test_split))
        test_data_expected_len = original_data_len - train_data_expected_len

        main.run(test_args)
        self.assertEqual(train_data_expected_len, len(pd.read_csv(test_args.out_data_file + '.train')))
        self.assertEqual(test_data_expected_len, len(pd.read_csv(test_args.out_data_file + '.test')))
