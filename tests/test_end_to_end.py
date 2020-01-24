from unittest import TestCase
import filecmp
import pandas as pd
import shutil
import os
import numpy as np

from shared_test_data import test_csv_filepath, test_asc_filepath, dict_to_obj

import main
import conf

tmpdir = 'tmp_test'
args = {k: v['default'] for k, v in conf.args_map.items()}
args['in_file'] = 'data/assistments2009-skill-builders-corrected_1000.csv'
args['out_file'] = tmpdir + '/tmp.tmp'
args['in_format'] = 'csv'
args['out_format'] = 'csv'
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
        test_args['out_file'] = tmpdir + '/tmp.csv'
        main.run(dict_to_obj(test_args))

        expected = pd.read_csv(test_args['in_file'])
        created = pd.read_csv(test_args['out_file'])
        print(expected)
        print(created)
        self.assertTrue(expected.equals(created))

    def test_from_tsv_equals_to_tsv(self):
        test_args = args.copy()
        test_args['out_file'] = tmpdir + '/tmp.tsv'
        main.run(dict_to_obj(test_args))

        expected = pd.read_csv(test_args['in_file'])
        created = pd.read_csv(test_args['out_file'])
        self.assertTrue(expected.equals(created))

    def test_from_csv_to_yudelson_bkt(self):
        test_args = args.copy()
        test_args['in_file'] = 'data/simple.csv'
        test_args['out_file'] = tmpdir + '/tmp.tsv'
        test_args['exercise_col'] = 'exercise_id'
        test_args['in_format'] = 'csv'
        test_args['out_format'] = 'yudelson_bkt'

        main.run(dict_to_obj(test_args))

        expected = pd.read_csv(test_args['in_file'])

        created = pd.read_csv(test_args['out_file'], sep='\t', header=None)

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
        test_args['in_file'] = 'data/test.asc'
        test_args['out_file'] = tmpdir + '/tmp.asc'
        test_args['in_format'] = 'asc'
        test_args['out_format'] = 'asc'
        main.run(dict_to_obj(test_args))

        self.assertTrue(filecmp.cmp(test_args['in_file'], test_args['out_file']))

    def test_train_test_split_creates_train_and_test_files(self):
        test_args = args.copy()
        test_args['test_rate'] = 0.2
        test_args = dict_to_obj(test_args)

        original_data_len = len(pd.read_csv(test_args.in_file))
        test_data_expected_len = int(original_data_len * test_args.test_rate)
        train_data_expected_len = original_data_len - test_data_expected_len

        main.run(test_args)
        self.assertEqual(train_data_expected_len, len(pd.read_csv(test_args.out_file + '.train')))
        self.assertEqual(test_data_expected_len, len(pd.read_csv(test_args.out_file + '.test')))

    def test_train_test_valid_split_creates_proper_files(self):
        test_args = args.copy()
        test_args['test_rate'] = 0.2
        test_args['validation_rate'] = 0.1
        test_args = dict_to_obj(test_args)

        original_data_len = len(pd.read_csv(test_args.in_file))
        test_data_expected_len = int(original_data_len * test_args.test_rate)
        validation_data_expected_len = int(original_data_len * test_args.validation_rate)
        train_data_expected_len = original_data_len - test_data_expected_len - validation_data_expected_len
        main.run(test_args)

        self.assertEqual(train_data_expected_len, len(pd.read_csv(test_args.out_file + '.train')))
        self.assertEqual(test_data_expected_len, len(pd.read_csv(test_args.out_file + '.test')))
        self.assertEqual(validation_data_expected_len, len(pd.read_csv(test_args.out_file + '.valid')))
