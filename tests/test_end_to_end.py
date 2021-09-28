from unittest import TestCase
import filecmp
import pandas as pd
import shutil
import os
import numpy as np
from shared_test_data import dict_to_obj, test_csv_filepath, test_simple_csv_filepath, test_asc_filepath

import converter
import arg_conf

tmpdir = 'tmp_test'
args = {k: v['default'] for k, v in arg_conf.converter_args_map.items()}
args['in-file'] = test_csv_filepath
args['out-file'] = tmpdir + '/tmp.tmp'
args['in-format'] = 'csv'
args['out-format'] = 'csv'
args['shuffle'] = 0


class EndToEndTest(TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(tmpdir): os.mkdir(tmpdir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(tmpdir)  # Remove this to check created files

    def test_from_csv_equals_to_csv(self):
        test_args = args.copy()
        test_args['out-file'] = tmpdir + '/tmp.csv'
        converter.fiddle(dict_to_obj(test_args))

        expected = pd.read_csv(test_args['in-file'])
        created = pd.read_csv(test_args['out-file'])
        print(expected)
        print(created)
        self.assertTrue(expected.equals(created))

    def test_from_tsv_equals_to_tsv(self):
        test_args = args.copy()
        test_args['out-file'] = tmpdir + '/tmp.tsv'
        converter.fiddle(dict_to_obj(test_args))

        expected = pd.read_csv(test_args['in-file'])
        created = pd.read_csv(test_args['out-file'])
        self.assertTrue(expected.equals(created))

    def test_from_csv_to_yudelson_bkt(self):
        test_args = args.copy()
        test_args['in-file'] = test_simple_csv_filepath
        test_args['out-file'] = tmpdir + '/tmp.tsv'
        test_args['exercise-col'] = 'exercise_id'
        test_args['in-format'] = 'csv'
        test_args['out-format'] = 'yudelson-bkt'

        converter.fiddle(dict_to_obj(test_args))

        expected = pd.read_csv(test_args['in-file'])

        created = pd.read_csv(test_args['out-file'], sep='\t', header=None)

        expected.correct = - (expected.correct - 1) + 1
        expected = expected[['correct', 'user_id', 'exercise_id', 'skill_id']]
        expected.user_id = 'student' + expected.user_id.astype(str)
        expected.exercise_id = 'exercise' + expected.exercise_id.astype(str)
        expected.skill_id = 'skill' + expected.skill_id.astype(str)

        print(expected)
        print(created)
        self.assertTrue(np.alltrue(expected.values == created.values))

    def test_from_asc_equals_to_asc(self):
        test_args = args.copy()
        test_args['in-file'] = test_asc_filepath
        test_args['out-file'] = tmpdir + '/tmp.asc'
        test_args['in-format'] = 'asc'
        test_args['out-format'] = 'asc'
        converter.fiddle(dict_to_obj(test_args))

        self.assertTrue(filecmp.cmp(test_args['in-file'], test_args['out-file']))

    def test_train_test_split_creates_train_and_test_files(self):
        test_args = args.copy()
        test_args['test-rate'] = 0.2
        test_args = dict_to_obj(test_args)

        original_data_len = len(pd.read_csv(test_args.in_file))
        test_data_expected_len = int(original_data_len * test_args.test_rate)
        train_data_expected_len = original_data_len - test_data_expected_len

        converter.fiddle(test_args)
        self.assertEqual(train_data_expected_len, len(pd.read_csv(test_args.out_file + '.train')))
        self.assertEqual(test_data_expected_len, len(pd.read_csv(test_args.out_file + '.test')))

    def test_train_test_valid_split_creates_proper_files(self):
        test_args = args.copy()
        test_args['test-rate'] = 0.2
        test_args['validation-rate'] = 0.1
        test_args = dict_to_obj(test_args)

        original_data_len = len(pd.read_csv(test_args.in_file))
        test_data_expected_len = int(original_data_len * test_args.test_rate)
        validation_data_expected_len = int(original_data_len * test_args.validation_rate)
        train_data_expected_len = original_data_len - test_data_expected_len - validation_data_expected_len
        converter.fiddle(test_args)

        self.assertEqual(train_data_expected_len, len(pd.read_csv(test_args.out_file + '.train')))
        self.assertEqual(test_data_expected_len, len(pd.read_csv(test_args.out_file + '.test')))
        self.assertEqual(validation_data_expected_len, len(pd.read_csv(test_args.out_file + '.valid')))
